from django.utils.translation import gettext_lazy as _

COUNTRIES_CHOICES = (
    ("BR", _("Brazil")),
    ("US", _("United States")),
)

ACTIVITY_TYPES = (
    ("CNF", _("Conference")),
    ("SCF", _("Special Conference")),
    ("ODD", _("Open Doors Day")),
    ("OTR", _("Others")),
)
