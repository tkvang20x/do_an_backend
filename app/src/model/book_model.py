from typing import Optional

from app.src.model.base.base_model import CustomBaseModel


class DetailBook(CustomBaseModel):
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
