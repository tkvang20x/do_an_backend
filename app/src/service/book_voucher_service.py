from datetime import datetime

from starlette import status

from app.src.base.base_exception import BusinessException, gen_exception_service
from app.src.base.base_service import Singleton
from app.src.model.book_model import UpdateBook
from app.src.model.book_voucher_model import VoucherCreate, VoucherDetail, VoucherUpdate
from app.src.repository.book_repository import BookRepository
from app.src.repository.book_voucher_repository import BookVoucherRepository
from app.src.repository.manager_repository import ManagerRepository
from app.src.repository.user_repository import UserRepository
from app.src.ultities import datetime_utils, const_utils, string_utils, mongo_utils
from app.src.ultities.const_utils import StatusVoucher


class BookVoucherService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()
        self.book_repo = BookRepository()
        self.voucher_repo = BookVoucherRepository()
        self.manager_repo = ManagerRepository()

    def create_voucher_service(self, data_create: VoucherCreate, user: str):
        try:
            data_create_dict = data_create.dict()
            data_create_convert = VoucherDetail(**data_create_dict)
            # self.user_repo.get_detail_user_repo(code=data_create_convert.user_id)

            for book in data_create_convert.books_borrowed:
                self.book_repo.get_detail_book_repo(code_id=book)

            data_create_convert.start_date = datetime_utils.get_string_datetime_now()
            data_create_convert.voucher_id = 'VOUCHER_' + str(datetime_utils.get_milisecond_time())
            data_create_convert.status_voucher = const_utils.StatusVoucher.WAITING_CONFIRM.value
            data_create_convert.modified_time = datetime_utils.get_string_datetime_now()

            user_result = self.user_repo.get_detail_user_repo(code=data_create_convert.user_id)
            manager_result = self.manager_repo.get_detail_manager_repo(code=user)

            data_create_convert.user_name = user_result.user_name

            data_create_convert.manager_name = manager_result.user_name
            data_create_convert.manager_id = manager_result.code
            data_create_convert.created_by = manager_result.user_name

            create_voucher_result = self.voucher_repo.create_voucher_repo(data_create=data_create_convert)
            if not create_voucher_result:
                raise RuntimeError(f'Create new voucher error!')

            for book in data_create_convert.books_borrowed:
                self.book_repo.update_book_repo(code_id=book, data_update=UpdateBook(status_borrow="BORROWING",
                                                                                     user_borrow=user_result.user_name))
            return create_voucher_result
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def get_list_voucher_by_user_id(self, user_id: str,
                                    voucher_id: str,
                                    user_name: str,
                                    page: int,
                                    size: int,
                                    order_by: str,
                                    order: int,
                                    start_date: str,
                                    due_date: str,
                                    status_voucher: str):
        try:
            filter_condition = self.build_filter_condition(user_id=user_id, voucher_id=voucher_id,
                                                           start_date=start_date, due_date=due_date,
                                                           status_voucher=status_voucher, user_name=user_name)
            list_book = self.voucher_repo.get_list_voucher_by_user_id_repo(
                page=page,
                size=size,
                order_by=order_by,
                order=order,
                filter_condition=filter_condition)
            return list_book
        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)

    def build_filter_condition(self, user_id: str, voucher_id: str, start_date: str, due_date: str, status_voucher: str,
                               user_name: str):
        filter_condition = {}
        if not string_utils.string_none_or_empty(user_id):
            filter_condition.update({'user_id': mongo_utils.build_filter_like_keyword(user_id.strip())})
        if not string_utils.string_none_or_empty(voucher_id):
            filter_condition.update({'voucher_id': mongo_utils.build_filter_like_keyword(voucher_id.strip())})
        if not string_utils.string_none_or_empty(start_date) and not string_utils.string_none_or_empty(due_date):
            filter_condition.update({"start_date": {"$gte": mongo_utils.build_filter_like_keyword(start_date.strip()),
                                                    "$lt": mongo_utils.build_filter_like_keyword(due_date.strip())}})
        if not string_utils.string_none_or_empty(user_name):
            filter_condition.update({'user_name': mongo_utils.build_filter_like_keyword(user_name.strip())})
        if not string_utils.string_none_or_empty(status_voucher):
            filter_condition.update({'status_voucher': status_voucher})

        return filter_condition

    def get_detail_voucher_service(self, voucher_id: str):
        try:
            voucher_data = self.voucher_repo.get_detail_voucher_repo(voucher_id=voucher_id)
            if not voucher_data:
                raise BusinessException(message=f'voucher by code [{voucher_id}] not exist!',
                                        http_code=status.HTTP_404_NOT_FOUND)
            return voucher_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_voucher_service(self, voucher_id: str, data_update: VoucherUpdate, user: str):
        try:
            self.get_detail_voucher_service(voucher_id=voucher_id.strip())
            if len(data_update.books_borrowed) > 0:
                for book_id in data_update.books_borrowed:
                    check_book = self.book_repo.get_detail_book_repo(code_id=book_id)
                    if check_book is None:
                        raise BusinessException(message=f'book by code [{book_id}] not exist!',
                                                http_code=status.HTTP_404_NOT_FOUND)
            data_update.modified_time = datetime_utils.get_string_datetime_now()
            manager_result = self.manager_repo.get_detail_manager_repo(code=user)
            data_update.modified_by = manager_result.user_name
            update_data = self.voucher_repo.update_voucher_repo(voucher_id=voucher_id, data_update=data_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def delete_voucher_service(self, voucher_id: str):
        try:
            self.get_detail_voucher_service(voucher_id=voucher_id.strip())
            delete_data = self.voucher_repo.delete_voucher_repo(voucher_id=voucher_id)
            if not delete_data:
                raise BusinessException(message=f'Delete voucher {voucher_id} remove fail!',
                                        http_code=status.HTTP_304_NOT_MODIFIED)
            return True
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def update_status_voucher_service(self, voucher_id: str, status_voucher: str):
        status_update = ""
        try:
            voucher_detail = self.get_detail_voucher_service(voucher_id=voucher_id.strip())
            if voucher_detail.status_voucher == StatusVoucher.WAITING_CONFIRM.value:
                status_update = StatusVoucher.CONFIRMED.value
            if voucher_detail.status_voucher == StatusVoucher.CONFIRMED.value:
                status_update = StatusVoucher.PAYED.value
            if voucher_detail.status_voucher == StatusVoucher.EXPIRED.value:
                status_update = StatusVoucher.PAYED.value
            if voucher_detail.status_voucher == StatusVoucher.PAYED.value:
                status_update = StatusVoucher.PAYED.value
            if status_voucher == StatusVoucher.CANCELLED.value:
                status_update = StatusVoucher.CANCELLED.value
            update_data = self.voucher_repo.update_status_voucher_repo(voucher_id=voucher_id,
                                                                       status_update=status_update)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)
