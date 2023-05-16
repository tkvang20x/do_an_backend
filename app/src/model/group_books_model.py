import json
from typing import Optional

from app.src.model.base.base_model import CustomBaseModel


class GroupBooks(CustomBaseModel):
    group_code: Optional[str] = None
    group_name: Optional[str] = None
    description: Optional[str] = None

    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate_to_json
    #
    # @classmethod
    # def validate_to_json(cls, value):
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value

class GroupBooksUpdate(CustomBaseModel):
    group_name: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value