import re
from unicodedata import normalize
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from datetime import date


COUNTRIES_CHOICES = [
    ("BR", _("Brazil")),
    ("US", _("United States")),
]

ACTIVITY_TYPES = [
    ("CNF", _("Conference")),
    ("ODD", _("Open Doors Day")),
    ("OTR", _("Others")),
]

EVENT_STATUS = [("OPN", _("open")), ("CLS", _("closed"))]

GENDER = [("M", _("Male")), ("F", _("Female"))]
BEDROOM_GENDER = [("M", _("Male")), ("F", _("Female")), ("X", _("Mixed"))]
BEDROOM_TYPE = [("B", _("Bottom")), ("T", _("Top"))]


ASPECTS = [
    ("PW", _("Public Work")),
    ("YW", _("Youth Work")),
    ("PG", _("Guest of Pupil")),
    ("A1", _("1st. Aspect")),
    ("A2", _("2st. Aspect")),
    ("A3", _("3st. Aspect")),
    ("A4", _("4st. Aspect")),
    ("GR", _("Grail")),
    ("A5", _("5st. Aspect")),
    ("A6", _("6st. Aspect")),
]

PAYMENT_TYPES = [
    ("CSH", _("Cash")),
    ("CHK", _("Check")),
    ("PRE", _("Pre Check")),
    ("DBT", _("Debit")),
    ("DPT", _("Deposit")),
    ("TRF", _("Transfer")),
    ("PIX", _("Pix")),
    ("FRE", _("Free")),
]

LODGE_TYPES = [("LDG", _("Lodge")), ("HSE", _("House")), ("HTL", _("Hotel"))]

"""
ARRIVAL_TIME | DEPARTURE_TIME | TAKE_MEAL

 "AEBD"
  └┼┼┼-> A = Arrive | D = Departure
   └┼┼-> E = Eve day | F = First day | L = Last day
    └┼-> B = Before | A = After
     └-> B = Breakfast | L = Lunch | D = Dinner
"""

ARRIVAL_TIME = [
    ("AEBD", _("Eve day, before dinner.")),
    ("AEAD", _("Eve day, after dinner.")),
    ("AFBB", _("First day, before breakfast.")),
    ("AFBL", _("First day, before lunch.")),
    ("AFBD", _("First day, before dinner.")),
    ("AFAD", _("First day, after dinner.")),
    ("ALBB", _("Last day, before breakfast.")),
]

DEPARTURE_TIME = [
    ("DFBL", _("First day, before lunch.")),
    ("DFBD", _("First day, before dinner.")),
    ("DFAD", _("First day, after dinner.")),
    ("DLBB", _("Last day, before breakfast.")),
    ("DLBL", _("Last day, before lunch.")),
    ("DLAL", _("Last day, after lunch.")),
]

TAKE_MEAL = {
    "AEBD": 0,  # eve dinner
    "AEAD": 1,  # 1 breakfast
    "AFBB": 1,  #     "
    "AFBL": 2,  # 1 lunch
    "AFBD": 3,  # 1 dinner
    "AFAD": 4,  # 2 breakfast
    "ALBB": 4,  #     "
    "DFBL": 1,  # 1 breakfast
    "DFBD": 2,  # 1 lunch
    "DFAD": 3,  # 1 dinner
    "DLBB": 3,  #     "
    "DLBL": 4,  # 2 breakfast
    "DLAL": 5,  # 2 lunch
}

"""
MEALS

 "MED"
  └┼┼-> M = Meal
   └┼-> E = Eve day | F = First day | L = Last day
    └-> B = Breakfast | L = Lunch | D = Dinner
"""

MEALS = {
    "MED": _("Dinner on the eve day"),
    "MFB": _("Breakfast on the first day"),
    "MFL": _("Lunch on the first day"),
    "MFD": _("Dinner on the first day"),
    "MLB": _("Breakfast on the last day"),
    "MLL": _("Lunch on the last day"),
}


# helpers
def us_inter_char(txt, codif="utf-8"):
    if not isinstance(txt, str):
        txt = str(txt)
    return (
        normalize("NFKD", txt)
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .lower()
    )


def short_name(name):
    words = name.split(" ")
    if len(words) <= 2:
        return name
    # get first and last words of name
    first_word = words[0]
    words.pop(0)
    last_word = words[-1]
    words.pop()
    # make a list to join
    to_join = [first_word]
    for word in words:
        if len(word) <= 3:
            to_join.append(word.lower())
        else:
            to_join.append(f"{word[0]}.")
    to_join.append(last_word)
    return " ".join(to_join)


def phone_format(num, country="BR"):
    num = (
        "+{}".format("".join(re.findall(r"\d", num)))
        if num.startswith("+")
        else "".join(re.findall(r"\d", num))
    )
    if not num:
        return ""
    if country == "BR":
        if num.startswith("+"):
            num = (
                f"+{num[1:3]} {num[3:5]} {num[5:10]}-{num[10:]}"
                if len(num) == 14
                else f"+{num[1:3]} {num[3:5]} {num[5:9]}-{num[9:]}"
            )
        elif len(num) in (10, 11):
            num = (
                f"+55 {num[:2]} {num[2:7]}-{num[7:]}"
                if len(num) == 11
                else f"+55 {num[:2]} {num[2:6]}-{num[6:]}"
            )
    return num


def clear_session(request, items):
    for item in items:
        if request.session.get(item):
            del request.session[item]


def get_bedroom_type(stay):
    if stay.no_bunk:
        return "B"
    if get_age(stay.person.birth) > 12 and get_age(stay.person.birth) < 45:
        return "T"
    else:
        return "B"


def get_age(birth):
    today = date.today()
    age = today.year - birth.year
    if today.month < birth.month or (
        today.month == birth.month and today.day < birth.day
    ):
        age -= 1
    return age


def get_paginator(request, queryset, quant=10):
    paginator = Paginator(queryset, quant)
    page_number = request.GET.get("page") or 1
    return paginator.get_page(page_number)


def get_pagination_url(request):
    preserved_qs = request.GET.copy()
    preserved_qs.pop("page", None)
    return f"{request.path}?{preserved_qs.urlencode()}"


def get_meals(stay):
    meals = [0, 0, 0, 0, 0, 0]
    if not stay.take_meals:
        return meals
    first_meal = TAKE_MEAL[stay.arrival_time]
    last_meal = TAKE_MEAL[stay.departure_time]
    if last_meal >= first_meal:
        meals[first_meal : last_meal + 1] = [
            1 for _ in meals[first_meal : last_meal + 1]
        ]
        return meals
    return meals
