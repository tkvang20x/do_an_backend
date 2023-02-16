import datetime

from fastapi import APIRouter, Request, Query
from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.book_voucher_model import VoucherCreate, VoucherUpdate
from app.src.service.book_voucher_service import BookVoucherService

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
def create_voucher(request: Request, data_create: VoucherCreate):
    try:
        response = voucher_service.create_voucher_service(data_create=data_create)
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
def update_voucher(request: Request, voucher_id: str, data_update: VoucherUpdate):
    try:
        response = voucher_service.update_voucher_service(voucher_id=voucher_id, data_update=data_update)
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