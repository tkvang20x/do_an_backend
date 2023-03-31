from enum import Enum


class StatusBook(Enum):
    NEW = 'NEW'
    OLD = 'OLD'


class StatusBorrow(Enum):
    BORROWING = 'BORROWING'
    READY = 'READY'
    WAITING = 'WAITING'


class StatusVoucher(Enum):
    WAITING_CONFIRM = 'WAITING_CONFIRM'
    CONFIRMED = 'CONFIRMED'
    PAYED = 'PAYED'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'
