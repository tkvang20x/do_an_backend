from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.model.group_books_model import GroupBooks, GroupBooksUpdate
from app.src.repository.books_repository import BooksRepository
from app.src.repository.group_books_repository import GroupBooksRepository
from app.src.ultities import datetime_utils, string_utils, mongo_utils


class GroupBooksService(metaclass=Singleton):
    def __init__(self):
        self.group_repo = GroupBooksRepository()
        self.books_repo = BooksRepository()

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

    def get_list_group_books(self, page: int,
                      size: int,
                      order_by: str,
                      order: int,
                      group_name: str):
        try:
            filter_condition = {}
            if not string_utils.string_none_or_empty(group_name):
                filter_condition.update({'group_name': mongo_utils.build_filter_like_keyword(group_name.strip())})

            list_book = self.group_repo.get_list_group_repo(page=page,
                                                          size=size,
                                                          order_by=order_by,
                                                          order=order,
                                                          filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_group_service(self, group_code: str, data_update: GroupBooksUpdate):
        try:
            update_data = self.group_repo.update_group_repo(group_code=group_code, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_group_service(self, group_code: str):
        try:
            update_data = self.group_repo.delete_group_repo(group_code= group_code)
            if not update_data:
                raise BusinessException(message=f'Delete group {group_code} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)

            update_books = self.books_repo.update_books_when_delete_groups(group_code=group_code)
            if not update_books:
                raise BusinessException(message=f'Update Group books: {group_code} in BOOKS_COLLECTION fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)

            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)