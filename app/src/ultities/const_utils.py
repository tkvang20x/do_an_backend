from enum import Enum


class StatusBook(Enum):
    NEW = 'NEW'
    OLD = 'OLD'


class StatusBorrow(Enum):
    BORROWING = 'BORROWING'
    READY = 'READY'


class StatusVoucher(Enum):
    WAITING_CONFIRM = 'WAITING_CONFIRM'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    PAYED = 'PAYED'
    EXPIRED = 'EXPIRED'
