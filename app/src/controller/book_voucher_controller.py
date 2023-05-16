import datetime
from typing import Optional

from fastapi import APIRouter, Request, Query, Depends
from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.book_voucher_model import VoucherCreate, VoucherUpdate, StatusVoucherUpdate
from app.src.service.book_voucher_service import BookVoucherService
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

voucher_service = BookVoucherService()


@router.get(path="/voucher", response_description="Get list voucher")
def get_list_voucher_by_user_id(request: Request,
                                page: int = 1,
                                size: int = 10,
                                order_by: str = Query(default="modified_time",
                                                      enum=["modified_time", "created_time"]),
                                order: int = Query(default=-1, enum=[-1, 1]),
                                user_id: str = None,
                                voucher_id: str = None,
                                user_name: str = None,
                                status_voucher: str = None,
                                start_date: str = None,
                                due_date: str = None):
    try:
        response = voucher_service.get_list_voucher_by_user_id(user_id=user_id,
                                                               page=page,
                                                               size=size,
                                                               order_by=order_by,
                                                               order=order,
                                                               voucher_id=voucher_id,
                                                               user_name=user_name,
                                                               start_date=start_date,
                                                               due_date=due_date,
                                                               status_voucher=status_voucher)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


@router.post(path="/voucher", response_description="Create new voucher")
def create_voucher(request: Request, data_create: VoucherCreate, user=Depends(validate_token)):
    try:
        response = voucher_service.create_voucher_service(data_create=data_create, user=user.get('code'))
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new voucher error. - Caused by: [{error_message}]")


@router.get(path="/voucher/{voucher_id}", response_description="Get detail voucher by code id")
def get_detail_voucher(request: Request, voucher_id: str):
    try:
        response = voucher_service.get_detail_voucher_service(voucher_id=voucher_id)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get detail book error. - Caused by: [{error_message}]")


@router.put(path="/voucher/{voucher_id}", response_description="Update voucher")
def update_voucher(request: Request, voucher_id: str, data_update: VoucherUpdate, user=Depends(validate_token)):
    try:
        response = voucher_service.update_voucher_service(voucher_id=voucher_id, data_update=data_update,
                                                          user=user.get('code'))
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update book error. - Caused by: [{error_message}]")


@router.put(path="/voucher/{voucher_id}/status", response_description="Update status voucher")
def update_status_voucher(request: Request, voucher_id: str, status_update: StatusVoucherUpdate):
    try:
        response = voucher_service.update_status_voucher_service(voucher_id=voucher_id,
                                                                 status_voucher=status_update.status_update)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update book error. - Caused by: [{error_message}]")


@router.delete(path="/voucher/{voucher_id}", response_description="Delete voucher")
def delete_voucher(request: Request, voucher_id: str):
    try:
        response = voucher_service.delete_voucher_service(voucher_id=voucher_id)
        return ResponseCommon().data(result=response, status=status.HTTP_204_NO_CONTENT, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Delete book error. - Caused by: [{error_message}]")


@router.get(path="/voucher-thongke1", response_description="Get list voucher")
def get_list_voucher_for_thong_ke(request: Request, month: str, year: str):
    try:
        response = voucher_service.get_list_voucher_for_thong_ke_1_month(month=month, year=year)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")
