import os

from fastapi import APIRouter, Request, Query, Depends, Body, UploadFile, File
from starlette import status
from fastapi.security import HTTPBearer
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.book_model import CreateBook
from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.service.book_service import BookService
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

book_service = BookService()
BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")


@router.get(path="/book/{code_books}", response_description="Get list book")
def get_list_book(request: Request,
                  code_books: str,
                  page: int = 1,
                  size: int = 10,
                  order_by: str = Query(default="modified_time",
                                        enum=["modified_time", "created_time"]),
                  order: int = Query(default=-1, enum=[-1, 1]),
                  status_book: str = None,
                  status_borrow: str = None,
                  user_borrow: str = None):
    try:
        response = book_service.get_list_book(page=page,
                                              size=size,
                                              order_by=order_by,
                                              order=order,
                                              code_books=code_books,
                                              status_book=status_book,
                                              status_borrow=status_borrow,
                                              user_borrow=user_borrow)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


# @router.post(path="/book/create", response_description="Create new book")
# def create_book(request: Request, data: CreateBook):
#     try:
#         response = book_service.create_book_service(data_create=data)
#         return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
#     except Exception as ex:
#         http_status, error_message = gen_exception_service(ex)
#         raise BusinessException(http_code=http_status,
#                                 path=request.url.path,
#                                 message=f"Create new book error. - Caused by: [{error_message}]")


# @router.get(path="/books/{code}", response_description="Get detail book")
# def get_detail_book(request: Request, code: str):
#     try:
#         response = books_service.get_detail_book_service(code=code)
#         return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
#     except Exception as ex:
#         http_status, error_message = gen_exception_service(ex)
#         raise BusinessException(http_code=http_status,
#                                 path=request.url.path,
#                                 message=f"Get detail book error. - Caused by: [{error_message}]")
#
#
# @router.put(path="/books/{code}", response_description="Update book")
# def update_book(request: Request, code: str, data_update: UpdateBookData = Body()):
#     try:
#         response = books_service.update_book_service(code=code, data_update=data_update)
#         return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
#     except Exception as ex:
#         http_status, error_message = gen_exception_service(ex)
#         raise BusinessException(http_code=http_status,
#                                 path=request.url.path,
#                                 message=f"Update book error. - Caused by: [{error_message}]")
#
#
# @router.delete(path="/books/{code}", response_description="Delete book")
# def delete_book(request: Request, code: str):
#     try:
#         response = books_service.delete_book_service(code=code)
#         return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
#     except Exception as ex:
#         http_status, error_message = gen_exception_service(ex)
#         raise BusinessException(http_code=http_status,
#                                 path=request.url.path,
#                                 message=f"Delete book error. - Caused by: [{error_message}]")
