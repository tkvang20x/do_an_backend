import os
import types

from fastapi import APIRouter, Request, Query, UploadFile, File
from starlette import status
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.user_model import CreateUser, UpdateUser
from app.src.service.user_service import UserService

router = APIRouter(
    route_class=BaseRoute
)

user_service = UserService()
BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")

@router.get(path="/users", response_description="Get list user")
def get_list_users(request: Request,
                   page: int = 1,
                   size: int = 10,
                   order_by: str = Query(default="modified_time",
                                         enum=["modified_time", "created_time"]),
                   order: int = Query(default=-1, enum=[-1, 1]),
                   name: str = None,
                   code: str = None):
    try:
        response = user_service.get_list_user(page=page,
                                              size=size,
                                              order_by=order_by,
                                              order=order,
                                              name=name,
                                              code=code)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list users. - Caused by: [{error_message}]")


@router.post(path="/users", response_description="Create new user")
def create_user(request: Request, data_create: CreateUser):
    try:
        response = user_service.create_user_service(data_create=data_create, user="")
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new user error. - Caused by: [{error_message}]")


@router.get(path="/users/{code}", response_description="Get detail user")
def get_detail_user(request: Request, code: str):
    try:
        response = user_service.get_detail_user_service(code=code)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get detail user error. - Caused by: [{error_message}]")


@router.put(path="/users/{code}", response_description="Update user")
def update_user(request: Request, code: str, data_update: UpdateUser):
    try:
        response = user_service.update_user_service(code=code, data_update=data_update)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")


@router.delete(path="/users/{code}", response_description="Delete user")
def delete_user(request: Request, code: str):
    try:
        response = user_service.delete_user_service(code=code)
        return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Delete user error. - Caused by: [{error_message}]")


@router.put(path="/users/{code}/avatar", response_description="Update avatar user")
async def update_user(request: Request, code: str, avatar: UploadFile = File(...)):
    try:
        response = await user_service.update_avatar_user_service(code=code, avatar=avatar, path_folder=BASEDIR)
        return ResponseCommon().data(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")
