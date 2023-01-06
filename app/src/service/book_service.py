from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_service import Singleton
from app.src.model.book_model import CreateBook, DetailBook
from app.src.repository.book_repository import BookRepository
from app.src.ultities import string_utils, mongo_utils, datetime_utils, const_utils
import time


class BookService(metaclass=Singleton):
    def __init__(self):
        self.book_repo = BookRepository()

    def get_list_book(self,
                      page: int,
                      size: int,
                      order_by: str,
                      order: int,
                      code_books: str,
                      status_book: str,
                      status_borrow: str,
                      user_borrow: str):
        try:
            filter_condition = self.build_filter_condition(code_books=code_books, status_book=status_book,
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

    def build_filter_condition(self, code_books: str, status_book: str, status_borrow: str, user_borrow: str):
        filter_condition = {'code_books': code_books}
        if not string_utils.string_none_or_empty(status_book):
            filter_condition.update({'status_book': mongo_utils.build_filter_like_keyword(status_book.strip())})
        if not string_utils.string_none_or_empty(status_borrow):
            filter_condition.update({'status_borrow': mongo_utils.build_filter_like_keyword(status_borrow.strip())})
        if not string_utils.string_none_or_empty(user_borrow):
            filter_condition.update({'user_borrow': mongo_utils.build_filter_like_keyword(user_borrow.strip())})
        return filter_condition

    def create_book_service(self, code_book: str):
        try:
            time.sleep(0.001)
            data_create = DetailBook()
            data_create.modified_time = datetime_utils.get_string_datetime_now()
            data_create.created_time = datetime_utils.get_string_datetime_now()
            data_create.code_id = "BOOK_" + str(datetime_utils.get_milisecond_time())
            data_create.code_books = code_book
            data_create.status_book = const_utils.StatusBook.NEW.value
            data_create.status_borrow = const_utils.StatusBorrow.READY.value
            create_book_result = self.book_repo.create_book_repo(data=data_create)
            if not create_book_result:
                raise RuntimeError(f'Create new book error!')
            return create_book_result
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)
