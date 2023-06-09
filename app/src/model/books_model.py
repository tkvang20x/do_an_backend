import json
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel
from app.src.model.group_books_model import GroupBooks


class DetailBooks(CustomBaseModel):
    id: Optional[str] = None
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
    total_ready: Optional[int] = 0
    group_code: Optional[str] = None
    groups: Optional[GroupBooks] = None
    cabinet: Optional[int] = 0


class ListBook(CustomBaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    author: Optional[str] = None
    avatar: Optional[str] = None
    total_books: Optional[int] = 0
    total_ready: Optional[int] = 0
    group_code: Optional[str] = None
    title: Optional[str] = None
    groups: Optional[GroupBooks] = None
    cabinet: Optional[int] = 0


class CreateDataBook(CustomBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    origin: Optional[str] = None
    group_code: Optional[str] = None
    amount: Optional[int] = None
    cabinet: Optional[int] = 0
    compartment: Optional[int] = 1

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UpdateBookData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    origin: Optional[str] = None
    group_code: Optional[str] = None
    cabinet: Optional[int] = 0

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UpdateBookDataFormService(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    name_university: Optional[str] = None
    publishing_year: Optional[str] = None
    origin: Optional[str] = None
    group_code: Optional[str] = None
    avatar: Optional[str] = None
    cabinet: Optional[int] = 0


class BooksFormInDB(CustomBaseModel):
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
    total_books_ready:Optional[str] = None
    cabinet: Optional[int] = 0
