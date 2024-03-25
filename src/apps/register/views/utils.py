import secrets
from datetime import datetime
from django.db.models import Q

from ..models import BankFlag
from apps.person.models import Person
from apps.event.models import Accommodation, Event
from r2e.commom import PAYMENT_TYPES


#  Helpers  ###################################################################
def init_session(request):
    request.session["order"] = {
        "order": None,
        "event": None,
        "event_center": None,
        "center": None,
        "alt_mapping": False,
        "registers": [],
        "payforms": [],
        "ref_value": 0.0,
        "total_registers": 0.0,
        "total_payforms": 0.0,
        "missing": 0.0,
    }


def get_dict_register(person, stay, ref_value, alt_mapping, event_id=None):
    bedroom = ""
    if stay:
        _bedroom = stay.bedroom_alt if alt_mapping else stay.bedroom

        query = Q(gender=person.gender) | Q(gender="X") & Q(
            bedroom_id=_bedroom
        )
        if event_id:
            query &= Q(event_id=event_id)

        accommodations = Accommodation.objects.filter(query)

        bedroom = _bedroom if accommodations else ""

    return dict(
        regid=stay.id if stay else secrets.token_hex(3)[:6],
        person=dict(name=person.name, id=person.id),
        lodge=(
            dict(name=stay.get_lodge_display(), id=stay.lodge) if stay else ""
        ),
        no_stairs=stay.no_stairs if stay else "",
        no_bunk=stay.no_bunk if stay else "",
        no_gluten=stay.no_gluten if stay else "",
        snorer=stay.snorer if stay else "",
        arrival_time=(
            dict(name=stay.get_arrival_time_display(), id=stay.arrival_time)
            if stay
            else ""
        ),
        departure_time=(
            dict(
                name=stay.get_departure_time_display(), id=stay.departure_time
            )
            if stay
            else ""
        ),
        take_meals=stay.take_meals if stay else None,
        meals=stay.meals if stay else [],
        staff=" | ".join([st.name for st in stay.staff.all()]) if stay else "",
        bedroom=bedroom,
        bedroom_type=stay.bedroom_type if stay else "",
        observations=stay.observations if stay else "",
        value=ref_value if stay else 0.0,
    )


def get_dict_register_update(register, event_center_pk, alt_mapping):
    person = register.person
    stay = person.stays.filter(stay_center__pk=event_center_pk).first()

    return dict(
        regid=stay.id,
        person=dict(name=register.person.name, id=register.person.id),
        lodge=dict(name=register.get_lodge_display(), id=register.lodge),
        no_stairs=register.no_stairs,
        no_bunk=register.no_bunk,
        no_gluten=register.no_gluten,
        snorer=register.snorer,
        arrival_time=dict(
            name=register.get_arrival_time_display(), id=register.arrival_time
        ),
        departure_time=dict(
            name=register.get_departure_time_display(),
            id=register.departure_time,
        ),
        take_meals=stay.take_meals,
        meals=stay.meals,
        staff=" | ".join([st.name for st in stay.staff.all()]) if stay else "",
        bedroom=(
            register.accommodation.bedroom_id if register.accommodation else ""
        ),
        bedroom_type=stay.bedroom_type,
        observations=register.observations,
        value=float(register.value),
    )


def get_dict_payform(payform):
    person = Person.objects.get(pk=payform["person"])
    bank_flag = (
        BankFlag.objects.get(pk=payform["bank_flag"])
        if payform["bank_flag"]
        else None
    )

    return dict(
        pfid=secrets.token_hex(3)[:6],
        person=dict(name=person.name, id=person.id),
        payment_type=dict(
            name=str(dict(PAYMENT_TYPES)[payform["payment_type"]]),
            id=payform["payment_type"],
        ),
        bank_flag=(
            dict(name=bank_flag.name, id=bank_flag.id) if bank_flag else ""
        ),
        ctrl=payform["ctrl"] or "",
        value=float(payform["value"]) or 0.0,
    )


def get_dict_payform_update(payform):
    return dict(
        pfid=payform.id,
        person=dict(name=payform.person.name, id=payform.person.id),
        payment_type=dict(
            name=str(dict(PAYMENT_TYPES)[payform.payment_type]),
            id=payform.payment_type,
        ),
        bank_flag=(
            dict(name=payform.bank_flag.name, id=payform.bank_flag.id)
            if payform.bank_flag
            else ""
        ),
        ctrl=payform.ctrl or "",
        value=float(payform.value) or 0.0,
    )


def get_register(order, regid):
    return [
        reg for reg in order["registers"] if str(reg["regid"]) == str(regid)
    ][0]


def get_payform(order, pfid):
    regs = [reg for reg in order["payforms"] if str(reg["pfid"]) == str(pfid)]

    return regs[0]


def adjust_missing_value(order):
    order["missing"] = order["total_payforms"] - order["total_registers"]


def total_registers_add(order, value):
    order["total_registers"] += value
    adjust_missing_value(order)


def total_registers_del(order, value):
    order["total_registers"] -= value
    if order["total_registers"] < 0:
        order["total_registers"] = 0.0
    adjust_missing_value(order)


def total_payforms_add(order, value):
    order["total_payforms"] += value
    adjust_missing_value(order)


def total_payforms_del(order, value):
    order["total_payforms"] -= value
    if order["total_payforms"] < 0:
        order["total_payforms"] = 0.0
    adjust_missing_value(order)


#   to save on database   #####################################################
def who_made_what(request, update):
    if update:
        return dict(updated_by=request.user)

    return dict(created_by=request.user, updated_by=request.user)


def get_dict_order_to_db(request, order, update=False):
    _order = dict(
        center_id=order["center"],
        event_id=order["event"],
        value=order["total_registers"],
        late_payment=datetime.now()
        > datetime.strptime(order["deadline"], "%Y-%m-%d %H:%M"),
        observations=request.POST.get("observations"),
    )
    _order.update(who_made_what(request, update))

    return _order


def get_event_days(event_id):
    event = Event.objects.get(pk=event_id)
    dt1, dt2 = event.date, event.end_date
    date_diff = dt2 - dt1
    return date_diff.days + 1


def get_dict_register_to_db(
    request, register, order_id, event_id, update=False
):
    event_days = get_event_days(event_id)

    meals = register["meals"]
    if event_days > 2:
        extra_days = event_days - 2
        to_take = (
            0
            if register["departure_time"]["id"] in ["DFBL", "DFBD", "DFAD"]
            else 1
        )
        for _ in range(extra_days * 3):
            meals.insert(4, to_take)

    _register = dict(
        person_id=register["person"]["id"],
        order_id=order_id,
        lodge=register["lodge"]["id"],
        no_stairs=register["no_stairs"],
        no_bunk=register["no_bunk"],
        no_gluten=register["no_gluten"],
        snorer=register["snorer"],
        arrival_time=register["arrival_time"]["id"],
        departure_time=register["departure_time"]["id"],
        take_meals=register["take_meals"],
        meals=meals,
        staff=register["staff"],
        observations=register["observations"],
        value=register["value"],
    )
    if register["bedroom"] and register["lodge"]["id"] == "LDG":
        try:
            accommodation = Accommodation.objects.filter(
                event_id=event_id,
                bedroom_id=register["bedroom"],
                bottom_or_top=register["bedroom_type"],
                register__isnull=True,
            )
        except Exception:
            accommodation = []
        _register["accommodation"] = (
            accommodation[0] if accommodation else None
        )
    _register.update(who_made_what(request, update))

    return _register


def get_dict_payforn_to_db(request, payform, order_id, update=False):
    _payform = dict(
        person_id=payform["person"]["id"],
        order_id=order_id,
        payment_type=payform["payment_type"]["id"],
        bank_flag_id=(
            payform["bank_flag"]["id"] if payform["bank_flag"] else None
        ),
        ctrl=payform["ctrl"] or None,
        value=payform["value"],
    )
    _payform.update(who_made_what(request, update))

    return _payform
