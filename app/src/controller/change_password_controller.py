from fastapi import APIRouter, Depends, Request, Body
from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.login_model import ChangePassWord
from app.src.service.change_password_service import ChangePasswordService
from app.src.ultities.token_utils import validate_token

router = APIRouter(
    route_class=BaseRoute
)

change_password_service = ChangePasswordService()


@router.put(path="/password", response_description="Update password")
def update_password(request: Request, new_pass: ChangePassWord, user=Depends(validate_token)):
    try:
        response = change_password_service.change_password_service(new_pass=new_pass.newpass, old_pass=new_pass.oldpass,
                                                                   username=user.get('username'), role=user.get('role'))
        if response:
            return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
        else:
            return ResponseCommon().success(result=response, status=status.HTTP_400_BAD_REQUEST, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")


@router.put(path="/forgot/{role}", response_description="Fotgot password")
def forgot_password(request: Request,role: str,email: str = Body(...)):
    try:
        response = change_password_service.forgot_password_service(email=email, role=role)
        return ResponseCommon().success(result=response, status=status.HTTP_200_OK, path=request.url.path)
    except Exception as ex:
        http_status, error_message = gen_exception_service(ex)
        raise BusinessException(http_code=http_status,
                                path=request.url.path,
                                message=f"Update user error. - Caused by: [{error_message}]")
