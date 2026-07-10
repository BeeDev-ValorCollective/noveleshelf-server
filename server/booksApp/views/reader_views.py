# booksApp/views/reader_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from booksApp.models import Book, BookPage, Chapter, UserBook, UserReadingProgress
from booksApp.serializers.reader_serializers import (
    UserBookSerializer, ChapterReadSerializer, ChapterLockedSerializer
)
from booksApp.views.public_views import format_book_summary
from userApp.models import UserWallet
from currencyApp.models import Transaction


# ─── Reading Sequence Assembly ───────────────────────────────────────────────

PAGE_TYPE_LABELS = {
    'dedication': 'Dedication',
    'acknowledgements': 'Acknowledgements',
    'authors_note': "Author's Note",
    'prologue': 'Prologue',
    'next_book_teaser': 'Next Book Teaser',
}

# Fixed reading-order position for each page_type relative to the chapters.
# 'before' pages appear in this order, ahead of chapter 1.
# 'after' pages appear in this order, following the final chapter.
PAGES_BEFORE_CHAPTERS = ['dedication', 'acknowledgements', 'authors_note', 'prologue']
PAGES_AFTER_CHAPTERS = ['next_book_teaser']


def assemble_reading_sequence(book, user):
    """
    Returns the full reading order for a book: published BookPages
    interleaved with published Chapters, per the fixed sequence:
    Dedication -> Acknowledgements -> Author's Note -> Prologue ->
    Chapters (in chapter_number order) -> Next Book Teaser.

    Pages have no unlock mechanic (no is_free/unlock_cost) — they're free
    whenever published, so their content is embedded directly here.
    Chapters stay metadata-only; content is fetched lazily (and possibly
    paywalled) via chapter_read/chapter_unlock.

    Each chapter entry is annotated with this user's is_unlocked/is_read
    progress (read-only lookup — does NOT create or mutate UserReadingProgress,
    unlike chapter_read) so the frontend can compute a resume point without
    triggering read/unlock side effects just by checking status.
    """
    pages_by_type = {
        p.page_type: p
        for p in BookPage.objects.filter(book=book, is_published=True)
    }

    progress_by_chapter_id = {
        p.chapter_id: p
        for p in UserReadingProgress.objects.filter(user=user, book=book)
    }

    sequence = []

    for page_type in PAGES_BEFORE_CHAPTERS:
        page = pages_by_type.get(page_type)
        if page:
            sequence.append({
                'type': 'page',
                'page_type': page.page_type,
                'title': PAGE_TYPE_LABELS.get(page.page_type, page.page_type),
                'content': page.content,
            })

    chapters = Chapter.objects.filter(
        book=book, status='published'
    ).order_by('chapter_number')

    for chapter in chapters:
        progress = progress_by_chapter_id.get(chapter.id)
        sequence.append({
            'type': 'chapter',
            'id': chapter.id,
            'chapter_number': chapter.chapter_number,
            'title': chapter.title,
            'display_title': (
                f'Chapter {chapter.chapter_number}: {chapter.title}'
                if chapter.title else f'Chapter {chapter.chapter_number}'
            ),
            'is_free': chapter.is_free,
            'unlock_cost': chapter.unlock_cost,
            'is_final': chapter.is_final,
            'word_count': chapter.word_count,
            'is_unlocked': bool(progress and progress.is_unlocked),
            'is_read': bool(progress and progress.is_read),
        })

    for page_type in PAGES_AFTER_CHAPTERS:
        page = pages_by_type.get(page_type)
        if page:
            sequence.append({
                'type': 'page',
                'page_type': page.page_type,
                'title': PAGE_TYPE_LABELS.get(page.page_type, page.page_type),
                'content': page.content,
            })

    return sequence


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
    plus shelf status, this reader's progress on the book (if any), and
    the full assembled reading_sequence (pages + chapters, in order).
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
    reading_sequence = assemble_reading_sequence(book, request.user)
    data['reading_sequence'] = reading_sequence

    # resume_index: position of the LAST is_read chapter in the sequence,
    # so the reading screen can land the reader back where they left off
    # rather than jumping ahead to the next unread chapter. 0 (very start,
    # including any lead-in pages) if nothing's been read yet.
    resume_index = 0
    for i, item in enumerate(reading_sequence):
        if item['type'] == 'chapter' and item['is_read']:
            resume_index = i
    data['resume_index'] = resume_index

    user_book = UserBook.objects.filter(user=request.user, book=book).first()
    data['in_shelf'] = user_book is not None
    data['progress'] = (
        {
            'completion_percentage': str(user_book.completion_percentage),
            'is_completed': user_book.is_completed,
            'completed_at': user_book.completed_at,
            'last_read_at': user_book.last_read_at,
            'auto_unlock_chapters': user_book.auto_unlock_chapters,
            'auto_unlock_prompted': user_book.auto_unlock_prompted,
        }
        if user_book else None
    )

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_auto_unlock_preference(request, book_id):
    """
    Sets this reader's auto-unlock preference for a specific book — asked
    once, the first time they hit a locked chapter in that book. Creates
    the UserBook row if it doesn't exist yet (shouldn't normally happen,
    since reaching a locked chapter implies they're already reading the
    book, but this keeps the endpoint safe to call regardless).

    Body: { "enabled": true }
    """
    book = get_object_or_404(Book, id=book_id)
    enabled = request.data.get('enabled')

    if enabled is None:
        return Response(
            {'error': 'enabled is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_book, _ = UserBook.objects.get_or_create(user=request.user, book=book)
    user_book.auto_unlock_chapters = bool(enabled)
    user_book.auto_unlock_prompted = True
    user_book.save(update_fields=['auto_unlock_chapters', 'auto_unlock_prompted'])

    return Response({
        'auto_unlock_chapters': user_book.auto_unlock_chapters,
        'auto_unlock_prompted': user_book.auto_unlock_prompted,
    })


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