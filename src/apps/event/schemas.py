from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from apps.accounts.models import CustomUser


@dataclass
class PayerSchema:
    center: str
    pg_type: str
    expected: Decimal
    person: str
    age: date
    payed: Decimal


@dataclass
class PayersSchema:
    pg_type: str
    payers: list
    payed: Decimal
    expected: Decimal

    @property
    def difference(self) -> Decimal:
        return self.payed - self.expected


@dataclass
class CollectedByCenterSchema:
    tax: Decimal
    center: str
    free: int = 0
    half: int = 0
    full: int = 0
    total_free: Decimal = Decimal(0.0)

    @property
    def total_half(self) -> Decimal:
        return self.tax / 2 * self.half

    @property
    def total_full(self) -> Decimal:
        return self.tax * self.full

    @property
    def total(self) -> Decimal:
        return (self.tax / 2 * self.half) + (self.tax * self.full)


@dataclass
class BedroomSchema:
    building: str
    id: int
    name: str
    gender: str
    floor: int
    bottom: int
    bottom_used: int
    bottom_free: int
    top: int
    top_used: int
    top_free: int
    used: int
    unused: int


@dataclass
class FormsOfPaymentSchema:
    order: int
    type: str
    bank_flag: str
    ctrl: str
    user: CustomUser
    on: date
    value: Decimal
