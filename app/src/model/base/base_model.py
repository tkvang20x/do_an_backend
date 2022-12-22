from typing import List, Optional

from pydantic import BaseModel, Field

from app.src.ultities import datetime_utils


class CustomBaseModel(BaseModel):
    is_active: Optional[bool] = Field(default=True)
    created_by: Optional[str] = Field(default="")
    created_time: Optional[str] = Field(default=datetime_utils.get_string_datetime_now())
    modified_time: Optional[str] = Field(default="")

def coor_response(response_data,
                  page: int = 0,
                  limit: int = 0,
                  sort_by: str = "",
                  sort: int = 0,
                  total_records: int = 0,
                  total_page: int = 0):
    """
        Build paging collection response
    :param collection_data:
    :param total_records:
    :param total_page:
    :return:
    """
    sort_mode = "asc" if sort == 1 else "desc"
    if isinstance(response_data, List):
        return {
            'result': response_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_records': total_records,
                'total_page': total_page
            },
            'sort': {
                'sort': sort_mode,
                'sort_by': sort_by
            }
        }
    else:
        return {
            'result': response_data,
            'pagination': {},
            'sort': {}
        }
