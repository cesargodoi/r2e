import re
from unicodedata import normalize
from django.utils.translation import gettext_lazy as _
from datetime import date


COUNTRIES_CHOICES = [
    ("BR", _("Brazil")),
    ("US", _("United States")),
]

ACTIVITY_TYPES = [
    ("CNF", _("Conference")),
    ("SCF", _("Special Conference")),
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

CREDIT_OPERATIONS = [
    ("ADJ", _("Adjustment")),
    ("GEN", _("Generation")),
    ("USE", _("Used")),
    ("CAN", _("Cancel")),
    ("EXC", _("Exclusion")),
    ("DEV", _("Devolution")),
    ("CML", _("Cancel Multiple")),
    ("RPY", _("Repayment")),
]

PAYMENT_TYPES = [
    ("CSH", _("Cash")),
    ("CHK", _("Check")),
    ("PRE", _("Pre Check")),
    ("DBT", _("Debit")),
    ("CDT", _("Credit")),
    ("DPT", _("Deposit")),
    ("TRF", _("Transfer")),
    ("GSC", _("Guest Credit")),
    ("FRE", _("Free")),
]

LODGE_TYPES = [("LDG", _("Lodge")), ("HSE", _("House")), ("HTL", _("Hotel"))]

ARRIVAL_DATE = [
    ("D0", _("Eve day")),
    ("D1", _("1st day")),
    ("D2", _("2nd day")),
]

ARRIVAL_TIME = [
    ("BB", _("Before breakfast")),
    ("BL", _("Before lunch")),
    ("BD", _("Before diner")),
    ("AD", _("After diner")),
]

DEPARTURE_TIME = [
    ("BL1", _("Before 1st lunch")),
    ("AL1", _("After 1st lunch")),
    ("BDN", _("Before dinner")),
    ("ADN", _("After dinner")),
    ("BL2", _("Before 2nd lunch")),
    ("AL2", _("After 2nd lunch")),
    ("END", _("End of event")),
]

STAFFS = [
    ("KIT", _("Kitchen")),
    ("DSW", _("Dishwashing")),
    ("REF", _("Refectory")),
    ("ACC", _("Accommodation")),
    ("EXT", _("External Area")),
    ("AFT", _("Aftermath")),
    ("SNK", _("Snack")),
    ("BRF", _("Breakfast")),
    ("TPL", _("Temple")),
    ("LDR", _("Laundry")),
    ("MTP", _("Multiple")),
    ("CNT", _("Center Team")),
]


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
    return (date.today() - birth).days // 365
