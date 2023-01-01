from fastapi import APIRouter, Request
from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.user_model import CreateUser
from app.src.service.user_service import UserService

router = APIRouter(
    route_class=BaseRoute
)

user_service = UserService()


@router.post(path="/users", response_description="Create new user")
def create_user(request: Request, data_create: CreateUser):
    try:
        response = user_service.create_user_service(data_create=data_create, user="")
        return ResponseCommon().success(result=response, status=status.HTTP_201_CREATED, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Create new book error. - Caused by: [{error_message}]")
