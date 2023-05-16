import types

from fastapi import UploadFile, File
from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.model.user_model import CreateUser, UpdateUser, DetailUser
from app.src.repository.user_repository import UserRepository
from app.src.ultities import datetime_utils, string_utils, mongo_utils, image_utils


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()

    def get_list_user(self,
                      page: int,
                      size: int,
                      order_by: str,
                      order: int,
                      name: str,
                      code: str,
                      role: str):
        try:
            filter_condition = self.build_filter_condition(name=name, code=code, role=role)
            list_book = self.user_repo.get_list_user_repo(page=page,
                                                          size=size,
                                                          order_by=order_by,
                                                          order=order,
                                                          filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition(self, name: str, code: str, role: str):
        filter_condition = {}
        if not string_utils.string_none_or_empty(name):
            filter_condition.update({'name': mongo_utils.build_filter_like_keyword(name.strip())})
        if not string_utils.string_none_or_empty(code):
            filter_condition.update({'code': code})
        if not string_utils.string_none_or_empty(role):
            filter_condition.update({'role': role})
        return filter_condition

    def create_user_service(self, data_create: CreateUser, user: ""):
        if self.user_repo.check_exist_value_in_db(field="user_name", value=data_create.user_name) is not None:
            raise BusinessException(
                message=f'User name existed!',
                http_code=status.HTTP_200_OK)

        if self.user_repo.check_exist_value_in_db(field="email", value=data_create.email) is not None:
            raise BusinessException(
                message=f'Email existed!',
                http_code=status.HTTP_200_OK)
        if self.user_repo.check_exist_value_in_db(field="code", value=data_create.code) is not None:
            raise BusinessException(
                message=f'Code existed!',
                http_code=status.HTTP_200_OK)

        data_create_dict = data_create.dict()
        data_create = DetailUser(**data_create_dict)
        data_create.modified_time = datetime_utils.get_string_datetime_now()
        data_create.created_time = datetime_utils.get_string_datetime_now()
        data_create.created_by = user
        # data_create.code = "USER_" + str(datetime_utils.get_timestamp_now())
        create_user_result = self.user_repo.create_user_repo(data_create=data_create)
        if not create_user_result:
            raise RuntimeError(f'Create new User error!')
        return create_user_result


    def get_detail_user_service(self, code: str):
        try:
            user_data = self.user_repo.check_exist_value_in_db(field="code", value=code)
            if not user_data:
                raise BusinessException(message=f'User by code [{code}] not exist!',
                                        http_code=status.HTTP_404_NOT_FOUND)
            return user_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_user_service(self, code: str, data_update: UpdateUser):
        try:
            self.get_detail_user_service(code=code.strip())
            update_data = self.user_repo.update_user_repo(code=code, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_user_service(self, code: str):
        try:
            self.get_detail_user_service(code=code.strip())
            update_data = self.user_repo.delete_user_repo(code=code)
            if not update_data:
                raise BusinessException(message=f'Delete user {code} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)
            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    @types.coroutine
    def update_avatar_user_service(self, code: str,path_folder: str, avatar: UploadFile = File(...)):
        try:
            self.get_detail_user_service(code=code.strip())

            path_avatar = yield from image_utils.create_upload_file(path_folder,avatar)
            update_avatar_data = self.user_repo.update_avatar_user_repo(code=code, path_avatar=path_avatar)
            return update_avatar_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)
