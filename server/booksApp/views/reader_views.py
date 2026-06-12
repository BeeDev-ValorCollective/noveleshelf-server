from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from booksApp.models import Book, Chapter, UserBook, UserReadingProgress
from booksApp.serializers.reader_serializers import (
    UserBookSerializer, ChapterReadSerializer, ChapterLockedSerializer
)
from userApp.models import UserWallet
from currencyApp.models import Transaction


# ─── Library ────────────────────────────────────────────────────────────────

class MyLibraryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

    def post(self, request):
        """Add a book to the reader's library."""
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'detail': 'book_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id, is_visible=True, status='approved')

        user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)

        if not created:
            return Response({'detail': 'Book is already in your library.'}, status=status.HTTP_200_OK)

        serializer = UserBookSerializer(user_book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyLibraryBookView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        """Remove a book from the reader's library."""
        user_book = get_object_or_404(UserBook, user=request.user, book_id=book_id)
        user_book.delete()
        return Response({'detail': 'Book removed from library.'}, status=status.HTTP_204_NO_CONTENT)


# ─── Chapter Read + Unlock ───────────────────────────────────────────────────

class ChapterReadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chapter_id):
        """
        Returns chapter content if accessible.
        Returns 402 with cost info if chapter needs unlocking.
        """
        chapter = get_object_or_404(
            Chapter.objects.select_related('book'),
            id=chapter_id,
            status='published'
        )

        # Check existing progress record
        progress = UserReadingProgress.objects.filter(
            user=request.user, chapter=chapter
        ).first()

        # Access granted if: chapter is free, OR already unlocked
        if chapter.is_free or (progress and progress.is_unlocked):
            # Mark as read
            if progress:
                if not progress.is_read:
                    progress.is_read = True
                    progress.read_at = timezone.now()
                    progress.save(update_fields=['is_read', 'read_at'])
            else:
                # Free chapter — create progress record
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
                # Auto-add to library if not already there
                UserBook.objects.get_or_create(user=request.user, book=chapter.book)

            serializer = ChapterReadSerializer(chapter)
            return Response(serializer.data)

        # Chapter needs unlocking — return cost info, no content
        serializer = ChapterLockedSerializer(chapter)
        return Response(
            {
                'locked': True,
                'chapter': serializer.data,
                'wallet': _wallet_summary(request.user),
            },
            status=status.HTTP_402_PAYMENT_REQUIRED
        )


class ChapterUnlockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chapter_id):
        """
        Deducts currency (black_ink → gold_ink → quills) and unlocks chapter.
        Frontend calls this after user confirms, then calls the read endpoint.
        """
        chapter = get_object_or_404(
            Chapter.objects.select_related('book'),
            id=chapter_id,
            status='published'
        )

        # Already unlocked?
        if UserReadingProgress.objects.filter(
            user=request.user, chapter=chapter, is_unlocked=True
        ).exists():
            return Response({'detail': 'Chapter already unlocked.'}, status=status.HTTP_200_OK)

        # Free chapter — shouldn't need this endpoint, but handle gracefully
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

        # Deduct in order: black_ink → gold_ink → quills
        # Track how much came from each for the transaction record
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

        # Determine primary currency type for UserReadingProgress
        # (the one that covered the most of the cost)
        if quill_used > 0 and quill_used >= black_used and quill_used >= gold_used:
            primary_currency = 'quills'
        elif gold_used > 0 and gold_used >= black_used:
            primary_currency = 'gold_ink'
        else:
            primary_currency = 'black_ink'

        # Write transaction records for each currency used
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

        # Create progress record
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

        # Auto-add to library if not already there
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