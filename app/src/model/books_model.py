from typing import Optional

from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel


class DetailBooks(CustomBaseModel):
    id: Optional[str] = None
    parent_id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    origin: Optional[str] = None
    avatar: Optional[str] = None
    total_books: Optional[int] = 0
    group_code: Optional[str] = None


class ListBook(CustomBaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    author: Optional[str] = None
    avatar: Optional[str] = None
    total_books: Optional[int] = None
    group_code: Optional[str] = None
    title: Optional[str] = None


class CreateDataBook(CustomBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    avatar: Optional[str] = None
    origin: Optional[str] = None
    group_code: Optional[str] = None
    amount: Optional[int] = None


class UpdateBookData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    avatar: Optional[str] = None
    origin: Optional[str] = None
    group_code: Optional[str] = None


class BooksFormInDB(CustomBaseModel):
    parent_id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    origin: Optional[str] = None
    avatar: Optional[str] = None
    group_code: Optional[str] = None
