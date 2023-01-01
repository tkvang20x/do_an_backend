from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.model.user_model import CreateUser
from app.src.repository.user_repository import UserRepository
from app.src.ultities import datetime_utils


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user_service(self, data_create: CreateUser, user: ""):
        data_create_dict = data_create.dict()
        data_create = CreateUser(**data_create_dict)
        data_create.modified_time = datetime_utils.get_string_datetime_now()
        data_create.created_time = datetime_utils.get_string_datetime_now()
        data_create.created_by = user
        data_create.user_id = "USER_" + str(datetime_utils.get_timestamp_now())
        create_user_result = self.user_repo.create_user_repo(data_create=data_create)
        if not create_user_result:
            raise RuntimeError(f'Create new User error!')
        return create_user_result
