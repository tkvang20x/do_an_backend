import types

from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_service import Singleton
from app.src.model.book_model import CreateBook, DetailBook, UpdateBook, UpdateUserBook
from app.src.repository.book_repository import BookRepository
from app.src.repository.books_repository import BooksRepository
from app.src.ultities import string_utils, mongo_utils, datetime_utils, const_utils, image_utils
import qrcode
import time


class BookService(metaclass=Singleton):
    def __init__(self):
        self.book_repo = BookRepository()
        self.books_reposiroty = BooksRepository()

    def get_list_book(self,
                      page: int,
                      size: int,
                      order_by: str,
                      order: int,
                      code_books: str,
                      code_id: str,
                      status_book: str,
                      status_borrow: str,
                      user_borrow: str):
        try:
            filter_condition = self.build_filter_condition(code_books=code_books, code_id=code_id,
                                                           status_book=status_book,
                                                           status_borrow=status_borrow, user_borrow=user_borrow)
            list_book = self.book_repo.get_list_book_repo(page=page,
                                                          size=size,
                                                          order_by=order_by,
                                                          order=order,
                                                          filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition(self, code_books: str, code_id: str, status_book: str, status_borrow: str,
                               user_borrow: str):
        filter_condition = {'code_books': code_books}
        if code_id is not None and len(code_id.strip()) > 0:
            filter_condition.update({'code_id': mongo_utils.build_filter_like_keyword(code_id.strip())})
        if status_book is not None and len(status_book.strip()) > 0:
            filter_condition.update({'status_book': status_book.strip()})
        if status_borrow is not None and len(status_borrow.strip()) > 0:
            filter_condition.update({'status_borrow': status_borrow.strip()})
        if user_borrow is not None and len(user_borrow.strip()) > 0:
            filter_condition.update({'user_borrow': mongo_utils.build_filter_like_keyword(user_borrow.strip())})
        return filter_condition

    @types.coroutine
    def create_book_service(self, code_books: str, path_folder: str, index: int,compartment: int):
        try:
            time.sleep(0.00000001)
            data_create = DetailBook()
            data_create.modified_time = datetime_utils.get_string_datetime_now()
            data_create.created_time = datetime_utils.get_string_datetime_now()
            data_create.code_id = "BOOK_" + str(datetime_utils.get_milisecond_time())
            data_create.code_books = code_books
            data_create.status_book = const_utils.StatusBook.NEW.value
            data_create.status_borrow = const_utils.StatusBorrow.READY.value
            data_create.serial = index
            data_create.compartment = compartment
            img_qrcode = qrcode.make(data_create.code_id)
            img_qrcode.save(f'{path_folder}\qrcode\{data_create.code_id}.png')
            data_create.qr_code_data = f'\qrcode\{data_create.code_id}.png'
            # create_book_result = self.book_repo.create_book_repo(data=data_create)

            create_book_result = self.book_repo.create_book_repo(data=data_create)
            if not create_book_result:
                raise RuntimeError(f'Create new book error!')
            return create_book_result
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    @types.coroutine
    def create_book_by_code_service(self, code_books: str, amount: int, compartment: int,path_folder: str):
        try:
            check_books = self.books_reposiroty.get_detail_book_repo(code=code_books)
            if check_books is None:
                raise BusinessException(message=f"Books {code_books} not found. - Caused by: [book_service]")
            if amount == 0 or amount is None:
                raise BusinessException(message=f"Amount book must have > 0. - Caused by: [book_service]")

            if check_books.total_books > 0:
                serial_book = check_books.total_books + 1
            else:
                serial_book = 1

            for i in range(amount):
                time.sleep(0.000001)
                data_create = DetailBook()
                data_create.modified_time = datetime_utils.get_string_datetime_now()
                data_create.created_time = datetime_utils.get_string_datetime_now()
                data_create.code_id = "BOOK_" + str(datetime_utils.get_milisecond_time())
                data_create.code_books = code_books
                data_create.status_book = const_utils.StatusBook.NEW.value
                data_create.status_borrow = const_utils.StatusBorrow.READY.value
                data_create.serial = serial_book
                data_create.compartment = compartment

                img_qrcode = qrcode.make(data_create.code_id)
                img_qrcode.save(f'{path_folder}\qrcode\{data_create.code_id}.png')
                data_create.qr_code_data = f'\qrcode\{data_create.code_id}.png'
                create_book_result = self.book_repo.create_book_repo(data=data_create)
                if not create_book_result:
                    raise RuntimeError(f'Create new book error!')
                serial_book = serial_book + 1
            return True
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def get_detail_book_service(self, code_id: str):
        try:
            book_data = self.book_repo.get_detail_book_repo(code_id=code_id)
            if not book_data:
                raise BusinessException(message=f'Book by code [{code_id}] not exist!',
                                        http_code=status.HTTP_404_NOT_FOUND)
            return book_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_book_service(self, code_id: str, data_update: UpdateBook):
        try:
            self.get_detail_book_service(code_id=code_id.strip())
            update_data = self.book_repo.update_book_repo(code_id=code_id, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_book_service(self, code_id: str):
        try:
            self.get_detail_book_service(code_id=code_id.strip())
            update_data = self.book_repo.delete_book_repo(code_id=code_id)
            if not update_data:
                raise BusinessException(message=f'Delete book {code_id} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)
            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def get_list_id_book(self, size: int, code_books: str, status_borrow: str):
        try:
            total_book_filter = self.book_repo.get_all_book_repo(code_books=code_books, status_borrow=status_borrow)
            if size > total_book_filter:
                raise BusinessException(message=f'Size > total book filter!',
                                        http_code=status.HTTP_400_BAD_REQUEST)

            filter_condition = self.build_filter_condition_2(code_books=code_books, status_borrow=status_borrow)

            list_book = self.book_repo.get_list_id_book_repo(size=size,
                                                             filter_condition=filter_condition)
            for item in list_book:
                self.book_repo.update_book_repo(code_id=item.get("code_id"), data_update=UpdateBook(user_borrow="",
                                                                                                    status_borrow=const_utils.StatusBorrow.WAITING.value))
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition_2(self, code_books: str, status_borrow: str):
        filter_condition = {'code_books': code_books}
        if status_borrow is not None and len(status_borrow.strip()) > 0:
            filter_condition.update({'status_borrow': mongo_utils.build_filter_like_keyword(status_borrow.strip())})
        return filter_condition

    def update_user_book_service(self, code_id: str, data_update:UpdateUserBook):
        try:
            self.get_detail_book_service(code_id=code_id.strip())
            update_data = self.book_repo.update_user_book_repo(code_id=code_id, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)