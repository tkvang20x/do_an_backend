import logging
import time
import uuid

from fastapi import Request
from starlette import status

from app.src.base.base_model import ResponseException


class BusinessException(Exception):
    def __init__(self, http_code=None, message=None, path=None):
        self.http_code = http_code if http_code else status.HTTP_400_BAD_REQUEST
        self.message = message
        self.path = path


async def error_handle_business(rp, ee):
    if isinstance(ee, BusinessException):
        http_code = ee.http_code
        message = ee.message
        path = ee.path
        return ResponseException().response(status=http_code,
                                            error_message=message,
                                            path=path)
    raise ee


def gen_exception_service(e: Exception,
                          default_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """
        Service exception handles
    :param default_status:
    :param e:
    :return:
    """
    http_status = default_status if not isinstance(e, BusinessException) else e.http_code
    error_message = e.__str__() if not isinstance(e, BusinessException) else e.message
    return http_status, error_message