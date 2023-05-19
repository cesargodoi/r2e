import secrets
from datetime import datetime

# from django.db.models import Q

from ..models import BankFlag
from apps.person.models import Person
from apps.event.models import Accommodation
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


def get_dict_register(person, stay, ref_value, alt_mapping):
    bedroom = stay.bedroom_alt if alt_mapping else stay.bedroom
    return dict(
        regid=stay.id if stay else secrets.token_hex(3)[:6],
        person=dict(name=person.name, id=person.id),
        lodge=dict(name=stay.get_lodge_display(), id=stay.lodge)
        if stay
        else "",
        no_stairs=stay.no_stairs if stay else "",
        no_bunk=stay.no_bunk if stay else "",
        arrival_date=dict(
            name=stay.get_arrival_date_display(), id=stay.arrival_date
        )
        if stay
        else "",
        arrival_time=dict(
            name=stay.get_arrival_time_display(), id=stay.arrival_time
        )
        if stay
        else "",
        departure_time=dict(
            name=stay.get_departure_time_display(), id=stay.departure_time
        )
        if stay
        else "",
        bedroom=bedroom if bedroom else "",
        bedroom_type=stay.bedroom_type if stay else "",
        observations=stay.observations if stay else "",
        value=ref_value if stay else 0.0,
    )


def get_dict_register_update(register, event_center_pk, alt_mapping):
    person = register.person
    stay = person.stays.filter(stay_center__pk=event_center_pk).first()
    return dict(
        regid=stay.id,
        person=dict(name=person.name, id=person.id),
        lodge=dict(name=register.get_lodge_display(), id=register.lodge),
        no_stairs=register.no_stairs,
        no_bunk=register.no_bunk,
        arrival_date=dict(
            name=register.get_arrival_date_display(), id=register.arrival_date
        ),
        arrival_time=dict(
            name=register.get_arrival_time_display(), id=register.arrival_time
        ),
        departure_time=dict(
            name=register.get_departure_time_display(),
            id=register.departure_time,
        ),
        bedroom=stay.bedroom_alt if alt_mapping else stay.bedroom,
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
        bank_flag=dict(name=bank_flag.name, id=bank_flag.id)
        if bank_flag
        else "",
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
        bank_flag=dict(name=payform.bank_flag.name, id=payform.bank_flag.id)
        if payform.bank_flag
        else "",
        ctrl=payform.ctrl or "",
        value=float(payform.value) or 0.0,
    )


def get_register(order, regid):
    return [
        reg for reg in order["registers"] if str(reg["regid"]) == str(regid)
    ][0]


def get_payform(order, pfid):
    print(type(pfid))
    return [reg for reg in order["payforms"] if str(reg["pfid"]) == str(pfid)][
        0
    ]


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
    else:
        return dict(created_by=request.user, updated_by=request.user)


def get_dict_order_to_db(request, order, update=False):
    _order = dict(
        center_id=order["center"],
        event_id=order["event"],
        value=order["total_registers"],
        late_payment=True
        if datetime.now()
        > datetime.strptime(order["deadline"], "%Y-%m-%d %H:%M")
        else False,
        observations=request.POST.get("observations"),
    )
    _order.update(who_made_what(request, update))
    return _order


def get_dict_register_to_db(request, register, order_id, update=False):
    _register = dict(
        person_id=register["person"]["id"],
        order_id=order_id,
        lodge=register["lodge"]["id"],
        no_stairs=register["no_stairs"],
        no_bunk=register["no_bunk"],
        arrival_date=register["arrival_date"]["id"],
        arrival_time=register["arrival_time"]["id"],
        departure_time=register["departure_time"]["id"],
        observations=register["observations"],
        value=register["value"],
    )
    # TODO: validar bedroom_alt  ?????
    if register["bedroom"]:
        try:
            accommodation = Accommodation.objects.filter(
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
        bank_flag_id=payform["bank_flag"]["id"]
        if payform["bank_flag"]
        else None,
        ctrl=payform["ctrl"] or None,
        value=payform["value"],
    )
    _payform.update(who_made_what(request, update))
    return _payform
