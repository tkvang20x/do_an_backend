from builtins import set
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
from app.src.service.change_password_service import ChangePasswordService


class BookVoucherService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()
        self.book_repo = BookRepository()
        self.voucher_repo = BookVoucherRepository()
        self.manager_repo = ManagerRepository()
        self.change_pass_service = ChangePasswordService()

    def create_voucher_service(self, data_create: VoucherCreate, user: str):
        try:
            list_id_book = []
            for item in data_create.books_borrowed:
                list_id_book.append(item.code_id)
            data_create.books_borrowed = list_id_book
            data_create_dict = data_create.dict()
            data_create_convert = VoucherDetail(**data_create_dict)
            # self.user_repo.get_detail_user_repo(code=data_create_convert.user_id)

            for book in data_create_convert.books_borrowed:
                # self.book_repo.get_detail_book_repo(code_id=book)
                dict_update = {
                    'status_borrow': const_utils.StatusBorrow.WAITING.value,
                    'user_borrow': user
                }
                self.book_repo.update_book_repo(code_id=book, data_update=UpdateBook(**dict_update))

            data_create_convert.start_date = datetime_utils.get_string_datetime_now()
            data_create_convert.voucher_id = 'VOUCHER_' + str(datetime_utils.get_milisecond_time())
            data_create_convert.status_voucher = const_utils.StatusVoucher.WAITING_CONFIRM.value
            data_create_convert.modified_time = datetime_utils.get_string_datetime_now()

            user_result = self.user_repo.check_exist_value_in_db(field="code", value=data_create_convert.user_id)
            # manager_result = self.manager_repo.get_detail_manager_repo(code=user)

            data_create_convert.user_name = user_result.user_name
            data_create_convert.email_user = user_result.email

            # data_create_convert.manager_name = manager_result.user_name
            # data_create_convert.manager_id = manager_result.code
            # data_create_convert.created_by = manager_result.user_name

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
                                    status_voucher: str,
                                    manager_name: str):
        try:
            filter_condition = self.build_filter_condition(user_id=user_id, voucher_id=voucher_id,
                                                           start_date=start_date, due_date=due_date,
                                                           status_voucher=status_voucher, user_name=user_name,
                                                           manager_name=manager_name)
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
                               user_name: str, manager_name: str):
        filter_condition = {}
        if not string_utils.string_none_or_empty(user_id):
            filter_condition.update({'user_id': mongo_utils.build_filter_like_keyword(user_id.strip())})
        if not string_utils.string_none_or_empty(voucher_id):
            filter_condition.update({'voucher_id': mongo_utils.build_filter_like_keyword(voucher_id.strip())})
        if not string_utils.string_none_or_empty(start_date) and not string_utils.string_none_or_empty(due_date):
            filter_condition.update({"start_date": {"$gte": start_date.strip(),
                                                    "$lt": due_date.strip()}})
        if not string_utils.string_none_or_empty(user_name):
            filter_condition.update({'user_name': mongo_utils.build_filter_like_keyword(user_name.strip())})
        if not string_utils.string_none_or_empty(status_voucher):
            filter_condition.update({'status_voucher': status_voucher})
        if not string_utils.string_none_or_empty(manager_name):
            filter_condition.update({'manager_name': mongo_utils.build_filter_like_keyword(manager_name.strip())})
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

    def update_status_voucher_service(self, voucher_id: str, status_voucher: str, manager: str):
        status_update = ""
        try:
            voucher_detail = self.get_detail_voucher_service(voucher_id=voucher_id.strip())
            list_book = voucher_detail.books_borrowed
            if status_voucher == StatusVoucher.CANCELLED.value:
                status_update = StatusVoucher.CANCELLED.value
                for book in list_book:
                    dict_update = {
                        'status_borrow': const_utils.StatusBorrow.READY.value,
                        'user_borrow': "",
                        'status_book': book.status_book,
                        'compartment': book.compartment
                    }
                    self.book_repo.update_book_repo(code_id=book.code_id, data_update=UpdateBook(**dict_update))

            elif voucher_detail.status_voucher == StatusVoucher.CONFIRMED.value:
                status_update = StatusVoucher.PAYED.value
                for book in list_book:
                    dict_update = {
                        'status_borrow': const_utils.StatusBorrow.READY.value,
                        'user_borrow': "",
                        'status_book': book.status_book,
                        'compartment': book.compartment
                    }
                    self.book_repo.update_book_repo(code_id=book.code_id, data_update=UpdateBook(**dict_update))
            else:
                if voucher_detail.status_voucher == StatusVoucher.WAITING_CONFIRM.value:
                    status_update = StatusVoucher.CONFIRMED.value
                elif voucher_detail.status_voucher == StatusVoucher.CONFIRMED.value:
                    status_update = StatusVoucher.PAYED.value
                elif voucher_detail.status_voucher == StatusVoucher.EXPIRED.value:
                    status_update = StatusVoucher.PAYED.value
                elif voucher_detail.status_voucher == StatusVoucher.PAYED.value:
                    status_update = StatusVoucher.PAYED.value

                for book in list_book:
                    dict_update = {
                        'status_borrow': const_utils.StatusBorrow.BORROWING.value,
                        'user_borrow': book.user_borrow,
                        'status_book': book.status_book,
                        'compartment': book.compartment
                    }
                    self.book_repo.update_book_repo(code_id=book.code_id, data_update=UpdateBook(**dict_update))
            update_data = self.voucher_repo.update_status_voucher_repo(voucher_id=voucher_id,
                                                                       status_update=status_update, manager=manager)
            return update_data
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def get_all_voucher_before_date_now(self):
        filter_date = {}
        date_now = datetime_utils.get_string_datetime_now()
        if not string_utils.string_none_or_empty(date_now):
            filter_date.update({"due_date": {"$lt": date_now.strip()},
                                "status_voucher": const_utils.StatusVoucher.CONFIRMED.value
                                })
        list_voucher = self.voucher_repo.get_list_voucher_by_user_id_repo(page=1, size=0, order_by="created_time",
                                                                          order=-1,
                                                                          filter_condition=filter_date)
        for item in list_voucher:
            self.voucher_repo.update_status_voucher_repo(voucher_id=item.voucher_id,
                                                         status_update=const_utils.StatusVoucher.EXPIRED.value,
                                                         manager=item.manager_name)

        filter_book_expired = {
            'status_voucher': const_utils.StatusVoucher.EXPIRED.value
        }
        list_voucher_expired = self.voucher_repo.get_list_voucher_by_user_id_repo(page=1, size=0,
                                                                                  order_by="created_time",
                                                                                  order=-1,
                                                                                  filter_condition=filter_book_expired)
        for item in list_voucher_expired:
            self.change_pass_service.send_email_message_expired(email=item.email_user, voucher_id=item.voucher_id)

    def get_list_voucher_for_thong_ke_1_month(self, month: str, year: str):
        try:
            filter_condition = {}

            date_end = datetime_utils.get_month_before_month_now(month=month)
            # year = datetime.now().year
            #
            # month_filter = month_now - month_amount
            # if month_filter == 0:
            #     month_filter = 12
            #     year = year - 1
            # elif 10 > month_filter > 0:
            #     month_filter = f'0{month_filter}'
            # filter_condition.update({"start_date": f'{year}-{month_filter}-01-00:00:00',
            #                          "due_date": f'{year}-{month_filter}-{date_end}-23:59:59'})

            filter_condition.update({"created_time": {"$gte": f'{year}-{month}-01-00:00:00',
                                                      "$lt": f'{year}-{month}-{date_end}-23:59:59'}})

            list_voucher = self.voucher_repo.get_list_voucher_by_user_id_repo(page=1, size=0, order_by='created_time',
                                                                              order=-1,
                                                                              filter_condition=filter_condition)

            list_books_count = []

            for item in list_voucher:
                for book in item.books_borrowed:
                    # if len(list_books_count) == 0:
                    #     list_books_count.append({
                    #         'code_books': book.get('code_books'),
                    #         'count': 1
                    #     })
                    if book.code_books not in [books.get('code_books') for books in list_books_count]:
                        list_books_count.append({
                            'code_books': book.code_books,
                            'name': book.books.name,
                            'author': book.books.author,
                            'avatar': book.books.avatar,
                            'count': 1
                        })
                    else:
                        for books in list_books_count:
                            if books.get('code_books') == book.code_books:
                                books.update({'count': books.get('count') + 1})
            new_list_sort = sorted(list_books_count, key=lambda i: i['count'], reverse=True)

            total_voucher, total_waiting, total_confirm, total_payed, total_expired, total_cancel = self.voucher_repo.get_list_voucher_for_thong_ke_1_month(
                filter_condition=filter_condition)

            return {"total_voucher": total_voucher,
                    "total_waiting": total_waiting,
                    "total_confirm": total_confirm,
                    "total_payed": total_payed,
                    "total_expired": total_expired,
                    "total_cancel": total_cancel,
                    "list_books_count": new_list_sort
                    }

        except Exception as ex:
            http_status, error_message = gen_exception_service(ex)
            raise BusinessException(message=error_message, http_code=http_status)
