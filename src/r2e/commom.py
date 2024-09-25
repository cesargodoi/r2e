import re
import phonenumbers

from unicodedata import normalize
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from datetime import date


COUNTRIES_CHOICES = [
    ("BR", _("Brazil")),
    ("BO", _("Bolivia")),
    ("AR", _("Argentina")),
    ("US", _("United States")),
    ("NL", _("Netherlands")),
    ("DE", _("Germany")),
    ("FR", _("France")),
    ("ES", _("Spain")),
    ("PT", _("Portugal")),
    ("IT", _("Italy")),
    ("OC", _("Other Country")),
]

ACTIVITY_TYPES = [
    ("CNF", _("Conference")),
    ("ODD", _("Open Doors Day")),
    ("OTR", _("Others")),
]

EVENT_STATUS = [
    ("OPN", _("open")),
    ("CLS", _("closed")),
    ("SRT", _("shortly")),
]

GENDER = [("M", _("Male")), ("F", _("Female"))]
BEDROOM_GENDER = [("M", _("Male")), ("F", _("Female")), ("X", _("Mixed"))]
BEDROOM_TYPE = [("B", _("Bottom")), ("T", _("Top"))]


ASPECTS = [
    ("21", _("Project 21")),
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
    ("CDT", _("Credit")),
    ("DPT", _("Deposit")),
    ("TRF", _("Transfer")),
    ("PIX", _("Pix")),
    ("FRE", _("Free")),
    ("PND", _("Pending")),
    ("PCD", _("Person Credit")),
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

"""
To calculate meals

meals = [0, 0, 0, 0, 0, 0]  # 0 = False   1 = True 

if not stay.take_meals:
    return meals

first_meal = TAKE_MEAL[stay.arrival_time]
last_meal = TAKE_MEAL[stay.departure_time]

meals[first_meal : len(meals) - last_meal] = [
    1 for _ in meals[first_meal : len(meals) - last_meal]
]
"""

TAKE_MEAL = {
    # arrival_time
    "AEBD": 0,  # eve dinner
    "AEAD": 1,  # 1 breakfast
    "AFBB": 1,  #     "
    "AFBL": 2,  # 1 lunch
    "AFBD": 3,  # 1 dinner
    "AFAD": 4,  # 2 breakfast
    "ALBB": 4,  #     "
    # departure_time
    "DFBL": 4,  # 1 breakfast
    "DFBD": 3,  # 1 lunch
    "DFAD": 2,  # 1 dinner
    "DLBB": 2,  #     "
    "DLBL": 1,  # 2 breakfast
    "DLAL": 0,  # 2 lunch
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

EXTRA_MEALS = {
    "M2B": _("Breakfast on the second day"),
    "M2L": _("Lunch on the second day"),
    "M2D": _("Dinner on the second day"),
    "M3B": _("Breakfast on the third day"),
    "M3L": _("Lunch on the third day"),
    "M3D": _("Dinner on the third day"),
    "M4B": _("Breakfast on the fourfth day"),
    "M4L": _("Lunch on the fourfth day"),
    "M4D": _("Dinner on the fourfth day"),
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
    words = name.strip().split(" ")
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
        if len(word) <= 3 and "." in word:
            to_join.append(word)
        elif len(word) <= 3:
            to_join.append(word.lower())
        else:
            to_join.append(f"{word[0]}.")
    to_join.append(last_word)
    return " ".join(to_join)


def phone_format(number, country="BR"):
    phone = PhoneBR(number)
    if phone.is_valid():
        return phone.format("int")
    else:
        return number


class PhoneBR:
    def __init__(self, number):
        try:
            self.number = phonenumbers.parse(number, "BR")
        except phonenumbers.NumberParseException as e:
            print(f"Erro ao parsear o número {number}: {e}")
            self.number = None

    def is_valid(self):
        if self.number is None:
            return False
        return phonenumbers.is_valid_number(self.number)

    def format(self, format):
        if self.number is None:
            return "---"
        match format:
            case "nat":
                return phonenumbers.format_number(
                    self.number, phonenumbers.PhoneNumberFormat.NATIONAL
                )
            case "int":
                return phonenumbers.format_number(
                    self.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
            case "e164":
                return phonenumbers.format_number(
                    self.number, phonenumbers.PhoneNumberFormat.E164
                )
            case _:
                return "---"


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

    if first_meal <= (len(meals) - last_meal - 1):
        meals[first_meal : len(meals) - last_meal] = [
            1 for _ in meals[first_meal : len(meals) - last_meal]
        ]
    return meals
