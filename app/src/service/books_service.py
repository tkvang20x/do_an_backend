import types

from fastapi import UploadFile, File
from starlette import status

from app.src.base.base_service import Singleton
from app.src.model.books_model import CreateDataBook, DetailBooks, UpdateBookData, UpdateBookDataFormService
from app.src.repository.books_repository import BooksRepository
from app.src.service.book_service import BookService
from app.src.service.group_books_service import GroupBooksService
from app.src.ultities import datetime_utils, string_utils, mongo_utils, image_utils
from app.src.base.base_exception import gen_exception_service, BusinessException


class BooksService(metaclass=Singleton):
    def __init__(self):
        self.books_repo = BooksRepository()
        self.book_repo = BookService()
        self.group_repo = GroupBooksService()

    @types.coroutine
    def create_books_service(self, data_create: CreateDataBook,avatar: UploadFile, path_folder: str, user: str = ""):
        try:
            amount = data_create.amount
            data_create_dict = data_create.dict()
            data_create = DetailBooks(**data_create_dict)
            data_create.modified_time = datetime_utils.get_string_datetime_now()
            data_create.created_time = datetime_utils.get_string_datetime_now()
            data_create.created_by = user
            data_create.code = "BOOKS_" + str(datetime_utils.get_timestamp_now())

            if avatar is not None:
                path_avatar = yield from image_utils.create_upload_file(path_folder, avatar)
                data_create.avatar = path_avatar

            create_book_result = self.books_repo.create_book_repo(data=data_create)
            if not create_book_result:
                raise RuntimeError(f'Create new Books error!')

            if amount > 0:
                for i in range(amount):
                    self.book_repo.create_book_service(code_books=data_create.code, path_folder=path_folder, index=i)

            return create_book_result
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def get_list_books(self,
                       page: int,
                       size: int,
                       order_by: str,
                       order: int,
                       name: str,
                       code: str,
                       author: str,
                       group_code: str):
        try:
            filter_condition = self.build_filter_condition(name=name, code=code, author=author, group_code=group_code)
            list_book = self.books_repo.get_list_book_repo(page=page,
                                                           size=size,
                                                           order_by=order_by,
                                                           order=order,
                                                           filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition(self, name: str, code: str, author: str, group_code: str):
        filter_condition = {}
        if name is not None and len(name.strip()) > 0:
            filter_condition.update({'name': mongo_utils.build_filter_like_keyword(name.strip())})
        if code is not None and len(code.strip()) > 0:
            filter_condition.update({'code': mongo_utils.build_filter_like_keyword(code.strip())})
        if author is not None and len(author.strip()) > 0:
            filter_condition.update({'author': mongo_utils.build_filter_like_keyword(author.strip())})
        if group_code is not None and len(group_code.strip()) > 0:
            filter_condition.update({'group_code': mongo_utils.build_filter_like_keyword(group_code.strip())})
        return filter_condition

    def get_detail_books_service(self, code: str):
        try:
            book_data = self.books_repo.get_detail_book_repo(code=code)
            if not book_data:
                raise BusinessException(message=f'Book by code [{code}] not exist!',
                                        http_code=status.HTTP_404_NOT_FOUND)
            return book_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    @types.coroutine
    def update_books_service(self, code: str, data_update: UpdateBookData, avatar:UploadFile, path_folder:str):
        try:
            detail_books = self.get_detail_books_service(code=code.strip())
            data_update_form_service = UpdateBookDataFormService(**data_update.dict())
            data_update_form_service.avatar = detail_books.avatar

            if avatar is not None:
                path_avatar = yield from image_utils.create_upload_file(path_folder, avatar)
                data_update_form_service.avatar = path_avatar
            update_data = self.books_repo.update_book_repo(code=code, data_update=data_update_form_service)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_books_service(self, code: str):
        try:
            self.get_detail_books_service(code=code.strip())
            update_data = self.books_repo.delete_book_repo(code=code)
            if not update_data:
                raise BusinessException(message=f'Delete book {code} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)
            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    @types.coroutine
    def update_avatar_books_service(self, code: str, path_folder: str, avatar: UploadFile = File(...)):
        try:
            self.get_detail_books_service(code=code.strip())

            path_avatar = yield from image_utils.create_upload_file(path_folder, avatar)
            update_avatar_data = self.books_repo.update_avatar_books_repo(code=code, path_avatar=path_avatar)
            return update_avatar_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)
