import secrets
from datetime import datetime

from ..models import BankFlag
from apps.person.models import Person
from r2e.commom import PAYMENT_TYPES


#  Helpers  ###################################################################
def init_session(request):
    request.session["new_order"] = {
        "event": None,
        "center": None,
        "registers": [],
        "payforms": [],
        "ref_value": 0.0,
        "total_registers": 0.0,
        "total_payforms": 0.0,
        "missing": 0.0,
    }


def get_dict_register(person, stay, ref_value):
    return dict(
        regid=stay.id if stay else secrets.token_hex(3)[:6],
        person=dict(name=person.name, id=person.id),
        lodge=dict(name=stay.get_lodge_display(), id=stay.lodge)
        if stay
        else "",
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
        no_stairs=stay.no_stairs if stay else "",
        no_bunk=stay.no_bunk if stay else "",
        observations=stay.observations if stay else "",
        value=ref_value if stay else 0.0,
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


def get_register(new_order, regid):
    return [
        reg
        for reg in new_order["registers"]
        if str(reg["regid"]) == str(regid)
    ][0]


def get_payform(new_order, pfid):
    print(type(pfid))
    return [
        reg for reg in new_order["payforms"] if str(reg["pfid"]) == str(pfid)
    ][0]


def adjust_missing_value(new_order):
    new_order["missing"] = (
        new_order["total_payforms"] - new_order["total_registers"]
    )


def total_registers_add(new_order, value):
    new_order["total_registers"] += value
    adjust_missing_value(new_order)


def total_registers_del(new_order, value):
    new_order["total_registers"] -= value
    if new_order["total_registers"] < 0:
        new_order["total_registers"] = 0.0
    adjust_missing_value(new_order)


def total_payforms_add(new_order, value):
    new_order["total_payforms"] += value
    adjust_missing_value(new_order)


def total_payforms_del(new_order, value):
    new_order["total_payforms"] -= value
    if new_order["total_payforms"] < 0:
        new_order["total_payforms"] = 0.0
    adjust_missing_value(new_order)


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
        observations=register["observations"],
        value=register["value"],
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