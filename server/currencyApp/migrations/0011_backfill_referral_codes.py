# currencyApp/migrations/0011_backfill_referral_codes.py
#
# Create this file with:
#   python manage.py makemigrations currencyApp --empty --name backfill_referral_codes
# Then replace its generated contents with everything below.

import random
import string

from django.db import migrations

CODE_LENGTH = 8
CODE_CHARS = string.ascii_uppercase + string.digits


def generate_unique_code(existing_codes):
    """
    Same generation logic as referral_utils.generate_referral_code,
    duplicated here because migrations shouldn't import app code
    directly (it can break if the model changes shape later).
    `existing_codes` is a running set checked in-memory to avoid a
    DB hit per candidate during a large backfill.
    """
    while True:
        candidate = ''.join(random.choices(CODE_CHARS, k=CODE_LENGTH))
        if candidate not in existing_codes:
            existing_codes.add(candidate)
            return candidate


def backfill_referral_codes(apps, schema_editor):
    User = apps.get_model('userApp', 'User')
    ReferralCode = apps.get_model('currencyApp', 'ReferralCode')

    existing_codes = set(
        ReferralCode.objects.values_list('code', flat=True)
    )

    users_missing_codes = User.objects.filter(
        referral_code__isnull=True
    )

    new_codes = [
        ReferralCode(
            user=user,
            code=generate_unique_code(existing_codes),
        )
        for user in users_missing_codes
    ]

    ReferralCode.objects.bulk_create(new_codes)


def reverse_noop(apps, schema_editor):
    # Deliberately not reversible -- deleting everyone's referral
    # codes on a rollback would break any codes already handed out.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('currencyApp', '0010_platformsettings_referral_reward_amount_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_referral_codes, reverse_noop),
    ]