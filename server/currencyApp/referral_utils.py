# currencyApp/referral_utils.py
import random
import string

CODE_LENGTH = 8
CODE_CHARS = string.ascii_uppercase + string.digits


def generate_referral_code():
    """
    Generates a random all-caps alphanumeric code, checking for
    collisions against existing ReferralCode rows. Mirrors the
    promo code generation pattern.
    """
    from .models import ReferralCode  # local import avoids circular import

    while True:
        candidate = ''.join(random.choices(CODE_CHARS, k=CODE_LENGTH))
        if not ReferralCode.objects.filter(code=candidate).exists():
            return candidate