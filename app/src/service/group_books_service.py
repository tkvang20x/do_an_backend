from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.model.group_books_model import GroupBooks
from app.src.repository.group_books_repository import GroupBooksRepository
from app.src.ultities import datetime_utils


class GroupBooksService(metaclass=Singleton):
    def __init__(self):
        self.group_repo = GroupBooksRepository()

    def create_group_books_service(self, data_create: GroupBooks):
        try:
            data_create.modified_time = datetime_utils.get_string_datetime_now()
            data_create.created_time = datetime_utils.get_string_datetime_now()
            data_create.created_by = ""
            data_create.group_code = "GROUPS_" + str(datetime_utils.get_timestamp_now())
            create_group_result = self.group_repo.create_group_repo(data=data_create)
            if not create_group_result:
                raise RuntimeError(f'Create new Group error!')
            return create_group_result
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)


    def get_list_group_books(self):
        try:
            list_book = self.group_repo.get_list_group_repo()
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)