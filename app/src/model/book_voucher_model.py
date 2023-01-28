from typing import Optional, List

from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel
from app.src.model.book_model import DetailBook
from app.src.model.user_model import DetailUser


class VoucherCreate(CustomBaseModel):
    books_borrowed: Optional[List[str]] = None
    due_date: Optional[str] = None
    user_id: Optional[str] = None
    manager_id: Optional[str] = None


class VoucherDetail(CustomBaseModel):
    voucher_id: Optional[str] = None
    manager_id: Optional[str] = None
    user_id: Optional[str] = None
    books_borrowed: Optional[List[str]] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    status_voucher: Optional[str] = None


class VoucherDetailOutDB(CustomBaseModel):
    voucher_id: Optional[str] = None
    manager_id: Optional[str] = None
    user_id: Optional[str] = None
    books_borrowed: Optional[List[str]] = None
    users: Optional[DetailUser] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    status_voucher: Optional[str] = None


class VoucherUpdate(BaseModel):
    books_borrowed: Optional[List[str]] = None
    due_date: Optional[str] = None
    manager_id: Optional[str] = None
    status_voucher: Optional[str] = None
