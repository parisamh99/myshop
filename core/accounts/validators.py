import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Matches:
# 0912xxxxxxx, 0990xxxxxxx, +98912xxxxxxx, 0098912xxxxxxx
IRAN_MOBILE_REGEX = re.compile(r'^(?:\+98|0098|0)?9\d{9}$')

def validate_iranian_mobile(value):
    """
    Validate Iranian cellphone (mobile) number.
    Acceptable formats:
      - 09123456789
      - +989123456789
      - 00989123456789
      - 9123456789 (without leading 0 or +98)
    """
    if not value:
        raise ValidationError(_('Enter a mobile number.'), code='invalid')

    # remove spaces, hyphens, and parentheses
    normalized = re.sub(r'[\s\-\(\)]', '', str(value))

    if IRAN_MOBILE_REGEX.fullmatch(normalized):
        return  # ✅ valid

    raise ValidationError(
        _('Enter a valid Iranian mobile number (e.g. 09123456789 or +989123456789).'),
        code='invalid'
    )
