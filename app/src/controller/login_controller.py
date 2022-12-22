from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import APIRouter, Request, HTTPException
from starlette import status

import jwt
import uvicorn
from app.src.base.base_exception import BusinessException
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from app.src.model.login_model import LoginRequest

router = APIRouter(
    route_class=BaseRoute
)

LOGIN_SUCCESS = "Login Success"
LOGIN_FAIL = "Login Fail"


def verify_password(username, password):
    if username == 'admin' and password == 'admin':
        return True
    return False


SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'


def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 30  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(request: Request, login: LoginRequest):
    response = verify_password(username=login.username, password=login.password)
    if response == True:
        token = generate_token(login.username)
        result = {
            'token': token
        }
        return ResponseCommon().success(result=result, status=status.HTTP_200_OK, path=request.url.path)
    else:
        raise BusinessException(http_code=404,
                                path=request.url.path,
                                message=f"LOGIN FAIL- NOT FOUND USER!")
