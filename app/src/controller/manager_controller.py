import os
import types

from fastapi import APIRouter, Request, Query, UploadFile, File, Form, Depends
from starlette import status
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.manager_model import CreateManager, UpdateManager
from app.src.model.user_model import CreateUser, UpdateUser
from app.src.service.manager_service import ManagerService
from app.src.service.user_service import UserService
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

manager_service = ManagerService()
BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")


@router.get(path="/managers", response_description="Get list manager")
def get_list_manager(request: Request,
                      page: int = 1,
                      size: int = 10,
                      order_by: str = Query(default="modified_time",
                                            enum=["modified_time", "created_time"]),
                      order: int = Query(default=-1, enum=[-1, 1]),
                      name: str = None,
                      code: str = None):
    try:
        response = manager_service.get_list_manager(page=page,
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


@router.post(path="/managers", response_description="Create new managers")
async def create_manager(request: Request, data: CreateManager = Form(...),avatar: UploadFile = File(...), user=Depends(validate_token)):
    try:
        if user.get('role') == 'USER' or user.get('role') == 'MANAGER':
            raise BusinessException(message=f'User not permission to access resource!',
                                    http_code=status.HTTP_403_FORBIDDEN)
        response = await manager_service.create_manager_service(data_create=data,avatar=avatar, path_folder=BASEDIR, user="")
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new user error. - Caused by: [{error_message}]")


@router.get(path="/managers/{code}", response_description="Get detail user")
def get_detail_manager(request: Request, code: str):
    try:
        response = manager_service.get_detail_manager_service(code=code)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get detail user error. - Caused by: [{error_message}]")


@router.put(path="/managers/{code}", response_description="Update user")
def update_manager(request: Request, code: str, data_update: UpdateManager):
    try:
        response = manager_service.update_manager_service(code=code, data_update=data_update)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")


@router.delete(path="/managers/{code}", response_description="Delete user")
def delete_manager(request: Request, code: str):
    try:
        response = manager_service.delete_manager_service(code=code)
        return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Delete user error. - Caused by: [{error_message}]")


@router.put(path="/managers/{code}/avatar", response_description="Update avatar user")
async def update_manager(request: Request, code: str, avatar: UploadFile = File(...)):
    try:
        response = await manager_service.update_avatar_manager_service(code=code, avatar=avatar, path_folder=BASEDIR)
        return ResponseCommon().data(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")
