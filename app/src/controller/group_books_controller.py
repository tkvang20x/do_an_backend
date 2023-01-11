from fastapi import APIRouter, Request
from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.group_books_model import GroupBooks
from app.src.service.group_books_service import GroupBooksService

router = APIRouter(
    route_class=BaseRoute
)

group_service = GroupBooksService()


@router.get(path="/groups", response_description="Get list group books")
def get_list_book(request: Request):
    try:
        response = group_service.get_list_group_books()
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Get list books. - Caused by: [{error_message}]")


@router.post(path="/groups", response_description="Create new group")
def create_group(request: Request, data_create: GroupBooks):
    try:
        response = group_service.create_group_books_service(data_create=data_create)
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new book error. - Caused by: [{error_message}]")