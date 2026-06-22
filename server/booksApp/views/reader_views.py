# booksApp/views/reader_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from booksApp.models import Book, Chapter, UserBook, UserReadingProgress
from booksApp.serializers.reader_serializers import (
    UserBookSerializer, ChapterReadSerializer, ChapterLockedSerializer
)
from booksApp.views.public_views import format_book_summary
from userApp.models import UserWallet
from currencyApp.models import Transaction


# ─── Library ────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_library(request):
    if request.method == 'GET':
        """List all books in the reader's library with progress."""
        user_books = (
            UserBook.objects
            .filter(user=request.user)
            .select_related(
                'book',
                'book__author_profile',
                'book__free_author_profile',
                'book__content_rating',
            )
            .prefetch_related('book__genres__genre')
            .order_by('-last_read_at', '-started_at')
        )
        serializer = UserBookSerializer(user_books, many=True, context={'request': request})
        return Response(serializer.data)

    # POST — add a book to the reader's library
    book_id = request.data.get('book_id')
    if not book_id:
        return Response({'detail': 'book_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    book = get_object_or_404(Book, id=book_id, is_visible=True, status='approved')

    user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)

    if not created:
        return Response({'detail': 'Book is already in your library.'}, status=status.HTTP_200_OK)

    serializer = UserBookSerializer(user_book, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def my_library_remove_book(request, book_id):
    """Remove a book from the reader's library."""
    user_book = get_object_or_404(UserBook, user=request.user, book_id=book_id)
    user_book.delete()
    return Response({'detail': 'Book removed from library.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_library_book_detail(request, book_id):
    """
    Reader-scoped book detail: same base data as the public detail view,
    plus shelf status and this reader's progress on the book (if any).
    """
    book = get_object_or_404(
        Book.objects.select_related(
            'content_rating',
            'author_profile',
            'author_profile__user',
            'free_author_profile',
            'free_author_profile__user',
        ).prefetch_related(
            'genres__genre',
            'relationship_tags__tag',
            'keywords__keyword',
        ),
        id=book_id,
        is_visible=True,
        status='approved',
    )

    chapters = Chapter.objects.filter(
        book=book,
        status='published'
    ).order_by('chapter_number').values(
        'id', 'chapter_number', 'title',
        'is_free', 'is_new', 'is_final', 'word_count',
        'unlock_cost', 'published_at'
    )

    chapters_data = []
    for chapter in chapters:
        chapter['display_title'] = (
            f'Chapter {chapter["chapter_number"]}: {chapter["title"]}'
            if chapter['title']
            else f'Chapter {chapter["chapter_number"]}'
        )
        chapters_data.append(chapter)

    data = format_book_summary(book)
    data['description'] = book.description or ''
    data['description_truncated'] = False
    data['chapters'] = chapters_data

    user_book = UserBook.objects.filter(user=request.user, book=book).first()
    data['in_shelf'] = user_book is not None
    data['progress'] = (
        {
            'completion_percentage': str(user_book.completion_percentage),
            'is_completed': user_book.is_completed,
            'completed_at': user_book.completed_at,
            'last_read_at': user_book.last_read_at,
        }
        if user_book else None
    )

    return Response(data)


# ─── Chapter Read + Unlock ───────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chapter_read(request, chapter_id):
    """
    Returns chapter content if accessible.
    Returns 402 with cost info if chapter needs unlocking.
    """
    chapter = get_object_or_404(
        Chapter.objects.select_related('book'),
        id=chapter_id,
        status='published'
    )

    progress = UserReadingProgress.objects.filter(
        user=request.user, chapter=chapter
    ).first()

    if chapter.is_free or (progress and progress.is_unlocked):
        if progress:
            if not progress.is_read:
                progress.is_read = True
                progress.read_at = timezone.now()
                progress.save(update_fields=['is_read', 'read_at'])
        else:
            UserReadingProgress.objects.create(
                user=request.user,
                book=chapter.book,
                chapter=chapter,
                is_unlocked=True,
                unlocked_at=timezone.now(),
                unlock_currency_type='free',
                is_read=True,
                read_at=timezone.now(),
            )
            UserBook.objects.get_or_create(user=request.user, book=chapter.book)

        serializer = ChapterReadSerializer(chapter)
        return Response(serializer.data)

    serializer = ChapterLockedSerializer(chapter)
    return Response(
        {
            'locked': True,
            'chapter': serializer.data,
            'wallet': _wallet_summary(request.user),
        },
        status=status.HTTP_402_PAYMENT_REQUIRED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chapter_unlock(request, chapter_id):
    """
    Deducts currency (black_ink → gold_ink → quills) and unlocks chapter.
    Frontend calls this after user confirms, then calls the read endpoint.
    """
    chapter = get_object_or_404(
        Chapter.objects.select_related('book'),
        id=chapter_id,
        status='published'
    )

    if UserReadingProgress.objects.filter(
        user=request.user, chapter=chapter, is_unlocked=True
    ).exists():
        return Response({'detail': 'Chapter already unlocked.'}, status=status.HTTP_200_OK)

    if chapter.is_free:
        return Response({'detail': 'This chapter is free — use the read endpoint directly.'}, status=status.HTTP_400_BAD_REQUEST)

    cost = chapter.unlock_cost
    if cost <= 0:
        return Response({'detail': 'Invalid unlock cost on this chapter.'}, status=status.HTTP_400_BAD_REQUEST)

    wallet, _ = UserWallet.objects.get_or_create(user=request.user)
    total_available = wallet.black_ink_balance + wallet.gold_ink_balance + wallet.quill_balance

    if total_available < cost:
        return Response(
            {
                'detail': 'Insufficient funds.',
                'wallet': _wallet_summary(request.user),
                'cost': cost,
            },
            status=status.HTTP_402_PAYMENT_REQUIRED
        )

    remaining = cost
    black_used = gold_used = quill_used = 0

    if wallet.black_ink_balance > 0 and remaining > 0:
        use = min(wallet.black_ink_balance, remaining)
        wallet.black_ink_balance -= use
        black_used = use
        remaining -= use

    if wallet.gold_ink_balance > 0 and remaining > 0:
        use = min(wallet.gold_ink_balance, remaining)
        wallet.gold_ink_balance -= use
        gold_used = use
        remaining -= use

    if wallet.quill_balance > 0 and remaining > 0:
        use = min(wallet.quill_balance, remaining)
        wallet.quill_balance -= use
        quill_used = use
        remaining -= use

    wallet.save()

    if quill_used > 0 and quill_used >= black_used and quill_used >= gold_used:
        primary_currency = 'quills'
    elif gold_used > 0 and gold_used >= black_used:
        primary_currency = 'gold_ink'
    else:
        primary_currency = 'black_ink'

    if black_used > 0:
        Transaction.objects.create(
            user=request.user,
            transaction_type='chapter_unlock',
            currency_type='black_ink',
            amount=-black_used,
            balance_after=wallet.black_ink_balance,
            notes=f'Unlocked chapter {chapter.chapter_number} of "{chapter.book.title}"'
        )
    if gold_used > 0:
        Transaction.objects.create(
            user=request.user,
            transaction_type='chapter_unlock',
            currency_type='gold_ink',
            amount=-gold_used,
            balance_after=wallet.gold_ink_balance,
            notes=f'Unlocked chapter {chapter.chapter_number} of "{chapter.book.title}"'
        )
    if quill_used > 0:
        Transaction.objects.create(
            user=request.user,
            transaction_type='chapter_unlock',
            currency_type='quills',
            amount=-quill_used,
            balance_after=wallet.quill_balance,
            notes=f'Unlocked chapter {chapter.chapter_number} of "{chapter.book.title}"'
        )

    UserReadingProgress.objects.update_or_create(
        user=request.user,
        chapter=chapter,
        defaults={
            'book': chapter.book,
            'is_unlocked': True,
            'unlocked_at': timezone.now(),
            'unlock_currency_type': primary_currency,
        }
    )

    UserBook.objects.get_or_create(user=request.user, book=chapter.book)

    return Response({
        'detail': 'Chapter unlocked.',
        'used': {
            'black_ink': black_used,
            'gold_ink': gold_used,
            'quills': quill_used,
        },
        'wallet': {
            'quill_balance': wallet.quill_balance,
            'gold_ink_balance': wallet.gold_ink_balance,
            'black_ink_balance': wallet.black_ink_balance,
        }
    }, status=status.HTTP_200_OK)


# ─── Helper ──────────────────────────────────────────────────────────────────

def _wallet_summary(user):
    try:
        w = user.wallet
        return {
            'quill_balance': w.quill_balance,
            'gold_ink_balance': w.gold_ink_balance,
            'black_ink_balance': w.black_ink_balance,
        }
    except Exception:
        return {'quill_balance': 0, 'gold_ink_balance': 0, 'black_ink_balance': 0}