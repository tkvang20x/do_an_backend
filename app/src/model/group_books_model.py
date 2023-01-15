from typing import Optional

from app.src.model.base.base_model import CustomBaseModel


class GroupBooks(CustomBaseModel):
    group_code: Optional[str] = None
    group_name: Optional[str] = None
    description: Optional[str] = None


class GroupBooksUpdate(CustomBaseModel):
    group_name: Optional[str] = None
    description: Optional[str] = None
