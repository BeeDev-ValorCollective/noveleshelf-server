from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    DailyLoginReward, Transaction, PlatformSettings,
    FoundingAuthorBonusTier, FoundingAuthorDuration,
    FoundingAuthorSlot, FoundingAuthorEligibleBook,
)


@admin.register(DailyLoginReward)
class DailyLoginRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_reward_date', 'total_earned', 'updated_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'currency_type', 'amount', 'balance_after', 'created_at']
    search_fields = ['user__email']
    list_filter = ['transaction_type', 'currency_type']
    readonly_fields = ['created_at']


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = ['daily_black_ink_reward', 'updated_at']


@admin.register(FoundingAuthorBonusTier)
class FoundingAuthorBonusTierAdmin(admin.ModelAdmin):
    list_display = ['percent']


@admin.register(FoundingAuthorDuration)
class FoundingAuthorDurationAdmin(admin.ModelAdmin):
    list_display = ['label', 'book_count']


class FoundingAuthorEligibleBookForm(forms.ModelForm):
    """
    Admin inline formsets do not call Model.full_clean() automatically —
    only ModelForm.clean() runs. Without this override, the book-count
    limit and author-match checks defined on
    FoundingAuthorEligibleBook.clean() are silently skipped when saving
    through the admin UI, even though they work correctly when called
    directly (e.g. via the API or a script).
    """
    class Meta:
        model = FoundingAuthorEligibleBook
        fields = ['slot', 'book']

    def clean(self):
        cleaned_data = super().clean()
        # Build a throwaway instance with the form's data so the model's
        # own clean() can run its checks against it, then surface any
        # ValidationError as a form-level error.
        instance = FoundingAuthorEligibleBook(
            pk=self.instance.pk,
            slot=cleaned_data.get('slot'),
            book=cleaned_data.get('book'),
        )
        if instance.slot_id and instance.book_id:
            try:
                instance.clean()
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return cleaned_data


class FoundingAuthorEligibleBookInline(admin.TabularInline):
    """
    Lets admin pick which books count toward a slot's bonus directly from
    the slot's detail page, instead of a separate flow. The custom form
    above ensures the book-count limit and author-match checks actually
    run when saving through this inline.
    """
    model = FoundingAuthorEligibleBook
    form = FoundingAuthorEligibleBookForm
    extra = 1
    autocomplete_fields = ['book']
    readonly_fields = ['assigned_at']

    def get_parent_object(self, request):
        """
        Recover the FoundingAuthorSlot being edited from the URL, since
        formfield_for_foreignkey only receives the request, not the
        parent object. Returns None on the "add new slot" page, where
        there's no parent yet to scope against.
        """
        resolved = request.resolver_match
        object_id = resolved.kwargs.get('object_id') if resolved else None
        if not object_id:
            return None
        return FoundingAuthorSlot.objects.filter(pk=object_id).select_related('author_profile').first()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'book':
            parent = self.get_parent_object(request)
            if parent and parent.author_profile_id:
                kwargs['queryset'] = db_field.related_model.objects.filter(
                    author_profile_id=parent.author_profile_id
                )
            else:
                # No author assigned yet (or this is the "add" page) --
                # nothing is a valid choice, since FoundingAuthorEligibleBook.clean()
                # requires the book's author to match the slot's author.
                kwargs['queryset'] = db_field.related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FoundingAuthorSlot)
class FoundingAuthorSlotAdmin(admin.ModelAdmin):
    list_display = [
        'slot_number', 'author_profile', 'bonus_tier', 'duration',
        'eligible_book_count', 'assigned_at',
    ]
    list_filter = ['bonus_tier', 'duration']
    search_fields = ['author_profile__pen_name', 'author_profile__author_username']
    autocomplete_fields = ['author_profile']
    readonly_fields = ['assigned_at', 'created_at', 'updated_at']
    inlines = [FoundingAuthorEligibleBookInline]
    ordering = ['slot_number']

    def eligible_book_count(self, obj):
        limit = obj.duration.book_count
        count = obj.eligible_books.count()
        if limit is None:
            return f'{count} (lifetime)'
        return f'{count} / {limit}'
    eligible_book_count.short_description = 'Books Assigned'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.author_profile:
            obj.author_profile.is_founding_author = True
            obj.author_profile.save(update_fields=['is_founding_author'])

    def delete_model(self, request, obj):
        if obj.author_profile:
            obj.author_profile.is_founding_author = False
            obj.author_profile.save(update_fields=['is_founding_author'])
        super().delete_model(request, obj)