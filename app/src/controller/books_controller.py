import os
from typing import Optional

from fastapi import APIRouter, Request, Query, Depends, Body, UploadFile, File, Form
from starlette import status
from fastapi.security import HTTPBearer
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.books_model import CreateDataBook, UpdateBookData
from app.src.service.books_service import BooksService
from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

books_service = BooksService()
BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")
app.mount("/qrcode", StaticFiles(directory=BASEDIR + "/qrcode"), name="qrcode")


@router.get(path="/books", response_description="Get list books")
def get_list_books(request: Request,
                   page: int = 1,
                   size: int = 10,
                   order_by: str = Query(default="modified_time",
                                         enum=["modified_time", "created_time"]),
                   order: int = Query(default=-1, enum=[-1, 1]),
                   name: str = None,
                   code: str = None,
                   author: str = None,
                   group_code: str = None,
                   user=Depends(validate_token)):
    try:
        response = books_service.get_list_books(page=page,
                                                size=size,
                                                order_by=order_by,
                                                order=order,
                                                name=name,
                                                code=code,
                                                author=author,
                                                group_code=group_code)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


@router.post(path="/books", response_description="Create new books")
async def create_books(request: Request, data: CreateDataBook = Form(...),avatar: UploadFile = File(...), user=Depends(validate_token)):
    try:
        if user.get('role') == 'USER':
            raise BusinessException(message=f'User not permission to access resource!',
                                    http_code=status.HTTP_403_FORBIDDEN)
        response = await books_service.create_books_service(data_create=data,avatar=avatar, path_folder=BASEDIR,user=user.get('username'))
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new book error. - Caused by: [{error_message}]")


@router.get(path="/books/{code}", response_description="Get detail books")
def get_detail_books(request: Request, code: str, user=Depends(validate_token)):
    try:
        response = books_service.get_detail_books_service(code=code)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get detail book error. - Caused by: [{error_message}]")


@router.put(path="/books/{code}", response_description="Update books")
async def update_books(request: Request, code: str, data_update: UpdateBookData = Form(...), avatar: UploadFile = File(None),user=Depends(validate_token)):
    try:
        # if user.get('role') == 'USER':
        #     raise BusinessException(message=f'User not permission to access resource!',
        #                             http_code=status.HTTP_403_FORBIDDEN)
        response = await books_service.update_books_service(code=code, data_update=data_update,avatar=avatar, path_folder=BASEDIR)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update book error. - Caused by: [{error_message}]")


@router.delete(path="/books/{code}", response_description="Delete books")
def delete_books(request: Request, code: str, user=Depends(validate_token)):
    try:
        response = books_service.delete_books_service(code=code)
        return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Delete book error. - Caused by: [{error_message}]")


@router.put(path="/books/{code}/avatar", response_description="Update avatar books")
async def update_books_avatar(request: Request, code: str, avatar: UploadFile = File(...), user=Depends(validate_token)):
    try:
        response = await books_service.update_avatar_books_service(code=code, avatar=avatar, path_folder=BASEDIR)
        return ResponseCommon().data(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")
