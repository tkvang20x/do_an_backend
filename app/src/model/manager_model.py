import json
from typing import Optional

from pydantic import BaseModel, validator

from app.src.model.base.base_model import CustomBaseModel, check_length_string


class CreateManager(CustomBaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = "MANAGER"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @validator('name', pre=True)
    def check_name(cls, value):
        check_length_string(name="name", value=value, max_length=32,
                            message_title="USER MODEL")
        return value

    @validator('course', pre=True)
    def check_course(cls, value):
        check_length_string(name="course", value=value, max_length=10,
                            message_title="USER MODEL")
        return value

    @validator('university', pre=True)
    def check_university(cls, value):
        check_length_string(name="university", value=value, max_length=100,
                            message_title="USER MODEL")
        return value

    @validator('phone', pre=True)
    def check_phone(cls, value):
        check_length_string(name="phone", value=value, max_length=10,
                            message_title="USER MODEL")
        return value

    @validator('email', pre=True)
    def check_email(cls, value):
        check_length_string(name="email", value=value, max_length=100,
                            message_title="USER MODEL")
        return value

    @validator('user_name', pre=True)
    def check_user_name(cls, value):
        check_length_string(name="user_name", value=value, max_length=32,
                            message_title="USER MODEL")
        return value

    @validator('password', pre=True)
    def check_password(cls, value):
        check_length_string(name="password", value=value, max_length=32,
                            message_title="USER MODEL")
        return value


class DetailManager(CustomBaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[str] = None


class ListManager(CustomBaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    avatar: Optional[str] = None


class UpdateManager(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    university: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
