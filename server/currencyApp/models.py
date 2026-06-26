from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class DailyLoginReward(models.Model):
    user = models.OneToOneField(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='daily_login_reward'
    )
    last_reward_date = models.DateField(null=True, blank=True)
    total_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} daily reward'


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('daily_login', 'Daily Login Reward'),
        ('ad_reward', 'Ad Reward'),
        ('quill_purchase', 'Quill Purchase'),
        ('chapter_unlock', 'Chapter Unlock'),
        ('author_payout', 'Author Payout'),
        ('admin_adjustment', 'Admin Adjustment'),
        ('admin_gift', 'Admin Gift'),
    ]

    CURRENCY_TYPES = [
        ('black_ink', 'Black Ink Drop'),
        ('gold_ink', 'Gold Ink Drop'),
        ('quills', 'Quills'),
    ]

    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPES)
    amount = models.IntegerField()
    balance_after = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.transaction_type} — {self.amount} {self.currency_type}'
    
class PlatformSettings(models.Model):
    daily_black_ink_reward = models.IntegerField(default=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Platform Settings'
        verbose_name_plural = 'Platform Settings'

    def __str__(self):
        return 'Platform Settings'


class FoundingAuthorBonusTier(models.Model):
    """The bonus percentage options — e.g. 10%, 5%. Admin can add more later."""
    percent = models.DecimalField(max_digits=4, decimal_places=2, unique=True)

    class Meta:
        ordering = ['-percent']
        verbose_name = 'Founding Author Bonus Tier'
        verbose_name_plural = 'Founding Author Bonus Tiers'

    def __str__(self):
        return f'{self.percent}%'


class FoundingAuthorDuration(models.Model):
    """
    The timeframe options — e.g. Lifetime (all books), First 5 Books, First 3 Books.

    book_count is the field business logic should key off of:
        book_count is None  -> lifetime, applies to every book
        book_count = 5      -> applies to the 5 books admin assigns to the slot
        book_count = 3      -> applies to the 3 books admin assigns to the slot

    `label` is display-only. Never branch logic on the label string —
    always check book_count.
    """
    label = models.CharField(max_length=50)
    book_count = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['book_count']
        verbose_name = 'Founding Author Duration'
        verbose_name_plural = 'Founding Author Durations'

    def __str__(self):
        return self.label


class FoundingAuthorSlot(models.Model):
    """
    A founding-author slot (1-40, expandable). Pre-seeded with the
    correct bonus_tier/duration per the client's breakdown table. Admin
    assigns an AuthorProfile to fill the slot, and can override the
    bonus_tier/duration per-slot if needed (e.g. "make slot #10 lifetime
    instead of first-3-books").

    Free authors are explicitly out of scope — this is a paid-author payout
    concern, so the FK only ever points to AuthorProfile.
    """
    slot_number = models.PositiveSmallIntegerField(unique=True)
    author_profile = models.OneToOneField(
        'userApp.AuthorProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='founding_author_slot',
    )
    bonus_tier = models.ForeignKey(
        FoundingAuthorBonusTier,
        on_delete=models.PROTECT,
        related_name='slots',
    )
    duration = models.ForeignKey(
        FoundingAuthorDuration,
        on_delete=models.PROTECT,
        related_name='slots',
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slot_number']
        verbose_name = 'Founding Author Slot'
        verbose_name_plural = 'Founding Author Slots'

    def __str__(self):
        who = self.author_profile.pen_name or self.author_profile.author_username if self.author_profile else 'Unassigned'
        return f'Slot #{self.slot_number} — {who}'

    def clean(self):
        # An AuthorProfile should only ever fill one slot.
        if self.author_profile_id:
            other = FoundingAuthorSlot.objects.filter(
                author_profile_id=self.author_profile_id
            ).exclude(pk=self.pk)
            if other.exists():
                raise ValidationError(
                    f'{self.author_profile} is already assigned to slot '
                    f'#{other.first().slot_number}.'
                )

    def save(self, *args, **kwargs):
        # Auto-stamp assigned_at the moment an author fills this slot.
        if self.author_profile_id and not self.assigned_at:
            self.assigned_at = timezone.now()
        elif not self.author_profile_id:
            self.assigned_at = None
        super().save(*args, **kwargs)


class FoundingAuthorEligibleBook(models.Model):
    """
    Which specific books count toward a book-limited slot's bonus
    (irrelevant for lifetime slots, where every book counts automatically).

    Admin assigns books by hand — if a book is later unpublished it simply
    stops earning (no special handling needed here), and admin can swap in
    a different book by the same author at any time.
    """
    slot = models.ForeignKey(
        FoundingAuthorSlot,
        on_delete=models.CASCADE,
        related_name='eligible_books',
    )
    book = models.ForeignKey(
        'booksApp.Book',
        on_delete=models.CASCADE,
        related_name='founding_author_eligibility',
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('slot', 'book')]
        verbose_name = 'Founding Author Eligible Book'
        verbose_name_plural = 'Founding Author Eligible Books'

    def __str__(self):
        return f'Slot #{self.slot.slot_number} — {self.book.title}'

    def clean(self):
        # The book should belong to the same author the slot is assigned to.
        # Checked first since a wrong-author book is invalid regardless of
        # whether the slot has room left.
        if self.slot.author_profile_id and self.book.author_profile_id:
            if self.slot.author_profile_id != self.book.author_profile_id:
                raise ValidationError(
                    'This book does not belong to the author assigned to this slot.'
                )

        # Enforce the slot's book_count limit (lifetime slots have no limit).
        limit = self.slot.duration.book_count
        if limit is not None:
            current_count = (
                FoundingAuthorEligibleBook.objects
                .filter(slot=self.slot)
                .exclude(pk=self.pk)
                .count()
            )
            if current_count >= limit:
                raise ValidationError(
                    f'Slot #{self.slot.slot_number} is limited to {limit} book(s) '
                    f'({current_count} already assigned).'
                )