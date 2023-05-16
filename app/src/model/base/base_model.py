import re
from typing import List, Optional

from pydantic import BaseModel, Field
from starlette import status

from app.src.base.base_exception import BusinessException
from app.src.ultities import datetime_utils

REGEX_STRING = '^(?!.*[^>]+>).*'


class CustomBaseModel(BaseModel):
    is_active: Optional[bool] = Field(default=True)
    is_delete: Optional[bool] = Field(default=False)
    created_by: Optional[str] = Field(default="")
    created_time: Optional[str] = Field(default=datetime_utils.get_string_datetime_now())
    modified_time: Optional[str] = Field(default="")
    modified_by: Optional[str] = Field(default="")


def check_length_array_string(name: str, list_value: List[str], max_length: int, message_title: str):
    if list_value:
        for value in list_value:
            if len(value) > max_length:
                raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                        message=f"{message_title} error. - Caused by: [ Field {name} item max length {max_length}! ]")


def check_bound_number(name: str, value: int, min_number: Optional[int], max_number: Optional[int], message_title: str):
    if min_number and value <= min_number:
        raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                message=f"{message_title} error. - Caused by: [ Field {name.upper()} must be larger {min_number}! ]")
    if max_number and value > max_number:
        raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                message=f"{message_title} error. - Caused by: [ Field {name.upper()} is not more than {max_number}! ]")


def check_length_string(name: str, value: str, max_length: int, message_title: str, min_length: Optional[int] = 1):
    # if len(value.strip()) == 0:
    #     raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
    #                             message=f"{message_title} error. - Caused by: [ {name.upper()} must not character! ]")
    if len(value) > max_length:
        raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                message=f"{message_title} error. - Caused by: [ {name.upper()} max length {max_length}! ]")
    # if len(value) < min_length:
    #     raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
    #                             message=f"{message_title} error. - Caused by: [ {name.upper()} min length {min_length}! ]")
    if not re.match(REGEX_STRING, value):
        raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                message=f"{message_title} error. - Caused by: [ Field {name.upper()} does not contain html! ]")


def check_regex(name: str, value: str, regex: str, message_title: str):
    pattern = regex
    if not re.match(pattern, value):
        raise BusinessException(http_code=status.HTTP_400_BAD_REQUEST,
                                message=f"{message_title} error. - Caused by: [ Field {name.upper()} is not in the correct format regex='{regex}'! ]")


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
