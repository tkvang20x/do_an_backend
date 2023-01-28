from fastapi import APIRouter, Request, HTTPException
from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.login_model import LoginRequest
from app.src.service.login_service import LoginService

router = APIRouter(
    route_class=BaseRoute
)

login_service = LoginService()


@router.post('/login/user')
def login(request: Request, login: LoginRequest):
    try:
        response = login_service.login_user(data_login=login)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"LOGIN FAIL- {error_message}!")
