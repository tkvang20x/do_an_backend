from starlette import status

from app.src.base.base_exception import BusinessException
from app.src.base.base_service import Singleton
from app.src.model.login_model import LoginRequest
from app.src.repository.manager_repository import ManagerRepository
from app.src.repository.user_repository import UserRepository
from datetime import datetime, timedelta
from typing import Union, Any
import jwt

LOGIN_SUCCESS = "LOGIN SUCCESS"
LOGIN_FAIL = "LOGIN FAIL"

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'


def generate_token(username: Union[str, Any], code: Union[str, Any], role: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 30  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, "username": username, "code": code, "role": role
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


class LoginService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()
        self.manager_repo = ManagerRepository()

    def login_user(self, data_login: LoginRequest):
        check_username = self.user_repo.check_user_name_user(user_name=data_login.username)
        if not check_username:
            raise BusinessException(message=f'User name {data_login.username} not exist!',
                                    http_code=status.HTTP_404_NOT_FOUND)

        if not data_login.password == check_username.password:
            raise BusinessException(message=f'PASSWORD INCORRECT !!!',
                                    http_code=status.HTTP_400_BAD_REQUEST)

        response = generate_token(check_username.user_name, check_username.code, check_username.role)
        response = {
            'token': response
        }
        return response

    def login_manager(self, data_login: LoginRequest):
        check_username = self.manager_repo.check_user_name_manager(user_name=data_login.username)
        if not check_username:
            raise BusinessException(message=f'User name {data_login.username} not exist!',
                                    http_code=status.HTTP_404_NOT_FOUND)

        if not data_login.password == check_username.password:
            raise BusinessException(message=f'PASSWORD INCORRECT !!!',
                                    http_code=status.HTTP_400_BAD_REQUEST)

        response = generate_token(check_username.user_name, check_username.code, check_username.role)
        response = {
            'token': response
        }
        return response
