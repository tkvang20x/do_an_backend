from typing import Optional

from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel


class DetailBook(CustomBaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    avatar: Optional[str] = None
    qr_code_data: Optional[str] = None
    amount: Optional[int] = None


class ListBook(CustomBaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    author: Optional[str] = None
    avatar: Optional[str] = None
    amount: Optional[int] = None


class CreateDataBook(CustomBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    avatar: Optional[str] = None
    amount: Optional[int] = None


class UpdateBookData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    avatar: Optional[str] = None
    amount: Optional[int] = None
