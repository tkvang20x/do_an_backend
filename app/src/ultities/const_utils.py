from enum import Enum


class StatusBook(Enum):
    NEW = 'NEW'
    OLD = 'OLD'


class StatusBorrow(Enum):
    BORROWING = 'BORROWING'
    READY = 'READY'
