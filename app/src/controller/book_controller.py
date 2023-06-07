import os

from fastapi import APIRouter, Request, Query, Depends, Body, UploadFile, File
from starlette import status
from fastapi.security import HTTPBearer
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.book_model import CreateBook, UpdateBook, CreateBookWithAmount, UpdateUserBook
from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.service.book_service import BookService
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

book_service = BookService()
BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")
app.mount("/qrcode", StaticFiles(directory=BASEDIR + "/qrcode"), name="qrcode")


@router.get(path="/book/{code_books}/list", response_description="Get list book")
def get_list_book(request: Request,
                  code_books: str,
                  page: int = 1,
                  size: int = 10,
                  order_by: str = Query(default="serial",
                                        enum=["modified_time", "created_time", "serial"]),
                  order: int = Query(default=-1, enum=[-1, 1]),
                  code_id: str = None,
                  status_book: str = None,
                  status_borrow: str = None,
                  user_borrow: str = None):
    try:
        response = book_service.get_list_book(page=page,
                                              size=size,
                                              order_by=order_by,
                                              order=order,
                                              code_books=code_books,
                                              code_id=code_id,
                                              status_book=status_book,
                                              status_borrow=status_borrow,
                                              user_borrow=user_borrow)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


@router.get(path="/book/listid/{code_books}", response_description="Get list book")
def get_list_id_book(request: Request,
                  code_books: str,
                  size: int = 5,
                  status_borrow: str = "READY"):
    try:
        response = book_service.get_list_id_book(size=size,
                                                 code_books=code_books,
                                                 status_borrow=status_borrow)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


@router.post(path="/book/create", response_description="Create new book")
def create_book(request: Request, data_create: CreateBookWithAmount):
    try:
        response = book_service.create_book_by_code_service(code_books=data_create.code_books, amount=data_create.amount,compartment=data_create.compartment ,path_folder=BASEDIR)
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new book error. - Caused by: [{error_message}]")


@router.get(path="/book/{code_id}", response_description="Get detail book by code id")
def get_detail_book(request: Request, code_id: str):
    try:
        response = book_service.get_detail_book_service(code_id=code_id)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get detail book error. - Caused by: [{error_message}]")


@router.put(path="/book/{code_id}", response_description="Update book")
def update_book(request: Request, code_id: str, data_update: UpdateBook):
    try:
        response = book_service.update_book_service(code_id=code_id, data_update=data_update)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update book error. - Caused by: [{error_message}]")


@router.delete(path="/book/{code_id}", response_description="Delete book")
def delete_book(request: Request, code_id: str):
    try:
        response = book_service.delete_book_service(code_id=code_id)
        return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Delete book error. - Caused by: [{error_message}]")


@router.put(path="/user-borrow/{code_id}", response_description="Update user borrow book")
def update_book(request: Request, code_id: str, data_update: UpdateUserBook):
    try:
        response = book_service.update_user_book_service(code_id=code_id, data_update=data_update)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update book error. - Caused by: [{error_message}]")