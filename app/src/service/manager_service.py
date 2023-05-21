import base64
import types

from fastapi import UploadFile, File
from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.model.manager_model import CreateManager, UpdateManager, DetailManager
from app.src.repository.manager_repository import ManagerRepository
from app.src.ultities import datetime_utils, string_utils, mongo_utils, image_utils


class ManagerService(metaclass=Singleton):
    def __init__(self):
        self.manager_repo = ManagerRepository()

    def get_list_manager(self,
                         page: int,
                         size: int,
                         order_by: str,
                         order: int,
                         name: str,
                         code: str, ):
        try:
            filter_condition = self.build_filter_condition(name=name, code=code)
            list_book = self.manager_repo.get_list_manager_repo(page=page,
                                                                size=size,
                                                                order_by=order_by,
                                                                order=order,
                                                                filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition(self, name: str, code: str):
        filter_condition = {}
        if not string_utils.string_none_or_empty(name):
            filter_condition.update({'name': mongo_utils.build_filter_like_keyword(name.strip())})
        if not string_utils.string_none_or_empty(code):
            filter_condition.update({'code': code})
        return filter_condition

    @types.coroutine
    def create_manager_service(self, data_create: CreateManager, avatar: UploadFile, path_folder: str, user: ""):
        data_create_dict = data_create.dict()
        data_create = DetailManager(**data_create_dict)
        data_create.modified_time = datetime_utils.get_string_datetime_now()
        data_create.created_time = datetime_utils.get_string_datetime_now()
        data_create.created_by = user
        data_create.code = "MANAGER_" + str(datetime_utils.get_timestamp_now())
        data_create.password = base64.b64encode(bytes(data_create.password, 'utf-8')).decode('utf-8')

        if avatar is not None:
            path_avatar = yield from image_utils.create_upload_file(path_folder, avatar)
            data_create.avatar = path_avatar
        create_user_result = self.manager_repo.create_manager_repo(data_create=data_create)
        if not create_user_result:
            raise RuntimeError(f'Create new User error!')
        return create_user_result

    def get_detail_manager_service(self, code: str):
        try:
            user_data = self.manager_repo.get_detail_manager_repo(code=code)
            if not user_data:
                raise BusinessException(message=f'User by code [{code}] not exist!',
                                        http_code=status.HTTP_404_NOT_FOUND)
            return user_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_manager_service(self, code: str, data_update: UpdateManager):
        try:
            self.get_detail_manager_service(code=code.strip())
            update_data = self.manager_repo.update_manager_repo(code=code, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_manager_service(self, code: str):
        try:
            self.get_detail_manager_service(code=code.strip())
            update_data = self.manager_repo.delete_manager_repo(code=code)
            if not update_data:
                raise BusinessException(message=f'Delete user {code} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)
            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    @types.coroutine
    def update_avatar_manager_service(self, code: str, path_folder: str, avatar: UploadFile = File(...)):
        try:
            self.get_detail_manager_service(code=code.strip())

            path_avatar = yield from image_utils.create_upload_file(path_folder, avatar)
            update_avatar_data = self.manager_repo.update_avatar_manager_repo(code=code, path_avatar=path_avatar)
            return update_avatar_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)
