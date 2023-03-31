from typing import Optional

from app.src.model.base.base_model import CustomBaseModel
from app.src.model.books_model import DetailBooks, BooksFormInDB
from app.src.model.group_books_model import GroupBooks


class ListBook(CustomBaseModel):
    code_id: Optional[str] = None
    code_books: Optional[str] = None
    status_book: Optional[str] = None
    status_borrow: Optional[str] = None
    user_borrow: Optional[str] = None
    qr_code_data: Optional[str] = None


class CreateBook(CustomBaseModel):
    code_id: Optional[str] = None
    code_books: Optional[str] = None
    status_book: Optional[str] = None
    qr_code_data: Optional[str] = None


class DetailBook(CustomBaseModel):
    id: Optional[str] = None
    code_id: Optional[str] = None
    code_books: Optional[str] = None
    books: Optional[BooksFormInDB]
    status_book: Optional[str] = None
    status_borrow: Optional[str] = None
    user_borrow: Optional[str] = None
    qr_code_data: Optional[str] = None
    groups: Optional[GroupBooks] = None


class UpdateBook(CustomBaseModel):
    # status_book: Optional[str] = None
    status_borrow: Optional[str] = None
    user_borrow: Optional[str] = None
