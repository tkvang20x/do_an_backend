from typing import Optional

from pydantic import BaseModel

from app.src.model.base.base_model import CustomBaseModel


class CreateUser(CustomBaseModel):
    name: Optional[str] = None
    user_id: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None

class DetailUser(CustomBaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    user_id: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_name: Optional[str] = None
