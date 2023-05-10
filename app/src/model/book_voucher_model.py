from typing import Optional, List

from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel
from app.src.model.book_model import DetailBook
from app.src.model.user_model import DetailUser


class BooksAmount(BaseModel):
    books_code: Optional[str] = None
    amount: Optional[int] = 0


class BookInVoucher(BaseModel):
    code_id: Optional[str] = None
    name_books: Optional[str] = None
    author: Optional[str] = None
    avatar: Optional[str] = None


class VoucherCreate(CustomBaseModel):
    books_borrowed: Optional[List[BookInVoucher]] = None
    due_date: Optional[str] = None
    user_id: Optional[str] = None
    description: Optional[str] = None


class VoucherDetail(CustomBaseModel):
    voucher_id: Optional[str] = None
    manager_id: Optional[str] = None
    user_id: Optional[str] = None
    books_borrowed: Optional[List[str]] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    status_voucher: Optional[str] = None
    description: Optional[str] = None
    user_name: Optional[str] = None
    email_user: Optional[str] = None
    manager_name: Optional[str] = None


class VoucherDetailOutDB(CustomBaseModel):
    voucher_id: Optional[str] = None
    manager_id: Optional[str] = None
    user_id: Optional[str] = None
    books_borrowed: Optional[List[str]] = None
    users: Optional[DetailUser] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    status_voucher: Optional[str] = None
    description: Optional[str] = None
    user_name: Optional[str] = None
    manager_name: Optional[str] = None


class VoucherUpdate(CustomBaseModel):
    books_borrowed: Optional[List[str]] = None
    due_date: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None


class StatusVoucherUpdate(BaseModel):
    status_update: Optional[str] = None
    # user_name: Optional[str] = None
