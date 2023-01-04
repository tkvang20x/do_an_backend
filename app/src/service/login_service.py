from starlette import status

from app.src.base.base_exception import BusinessException
from app.src.base.base_service import Singleton
from app.src.model.login_model import LoginRequest
from app.src.repository.user_repository import UserRepository
from datetime import datetime, timedelta
from typing import Union, Any
import jwt

LOGIN_SUCCESS = "LOGIN SUCCESS"
LOGIN_FAIL = "LOGIN FAIL"

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


class LoginService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()

    def login_user(self, data_login: LoginRequest):
        check_username = self.user_repo.check_user_name_user(user_name=data_login.username)
        if not check_username:
            raise BusinessException(message=f'User name {data_login.username} not exist!',
                                    http_code=status.HTTP_404_NOT_FOUND)
        response = generate_token(data_login.username)
        return response
