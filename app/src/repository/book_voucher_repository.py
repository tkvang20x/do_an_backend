import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.book_voucher_model import VoucherCreate, VoucherDetail, VoucherDetailOutDB, VoucherUpdate
from app.src.repository.book_repository import BookRepository
from app.src.ultities import mongo_utils, collection_utils, datetime_utils

VOUCHER_COLLECTION = 'voucher'


class BookVoucherRepository(MongoBaseRepo):
    def __init__(self):
        super(BookVoucherRepository, self).__init__(VOUCHER_COLLECTION)
        self.voucher_collection = self.collection
        self._record_status_active = {'is_active': True}
        self.book_repo = BookRepository()

    def create_voucher_repo(self, data_create: VoucherDetail):
        try:
            create_data = data_create.dict()
            if 'id' in create_data:
                del create_data['id']

            self.voucher_collection.insert_one(create_data)
            voucher_result_dict = self._dict_to_voucher_result(create_data)
            return voucher_result_dict
        except Exception as e:
            logging.error(f"Create voucher error! -- Caused by '{e.__str__()}")
            return None

    def _dict_to_voucher_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        result = VoucherDetail(**dict_object_id)
        for i in range(len(result.books_borrowed)):
            book_data = self.book_repo.get_detail_book_repo(result.books_borrowed[i])
            result.books_borrowed[i] = book_data

        return result

    def get_list_voucher_by_user_id_repo(self, page: int,
                                         size: int,
                                         order_by: str,
                                         order: int,
                                         filter_condition: dict):
        try:
            # init data
            total = 0
            total_page = 0
            skip = (page - 1) * size
            # build filter condition
            # Get list ocr_engine by condition
            filter_condition.update(self._record_status_active)

            # filter_aggregation = {'$match': {'is_active': True}}
            # sort_aggregation = {'$sort': {f'{order_by}': order}}
            # skip_aggregation = {'$skip': skip}
            # size_aggregation = {'$limit': size}
            #
            # # build query
            # querry_command = [
            #     filter_aggregation,
            #     sort_aggregation,
            #     skip_aggregation,
            #     size_aggregation,
            # ]

            # get full result dict
            # list_voucher_result_dict = list(self.voucher_collection.aggregate(querry_command))

            list_voucher_result_dict = list(
                self.voucher_collection.find(filter_condition).sort([(order_by, order)]).skip(skip).limit(size))
            if collection_utils.list_none_or_empty(list_voucher_result_dict):
                list_voucher = []
            else:
                list_voucher = [self._dict_to_voucher_result(voucher) for voucher in
                                list_voucher_result_dict]

            # count total
            total = self.voucher_collection.count_documents(filter_condition)
            # calculate total page
            if not total or total == 0:
                total_page = 0
            else:
                total_page = ((total + size - 1) // size)
            result_pagnition = base_model.coor_response(response_data=list_voucher,
                                                        page=page,
                                                        limit=size,
                                                        sort_by=order_by,
                                                        sort=order,
                                                        total_records=total,
                                                        total_page=total_page)

            return result_pagnition
        except Exception as e:
            logging.error(f"Get List OCR Engine error -- Caused by '{e.__str__()}")
            return None

    def get_detail_voucher_repo(self, voucher_id: str):
        filter_aggregation = {'$match': {'is_active': True, 'voucher_id': voucher_id}}

        user_lookup = {'$lookup': {
            "from": "users",
            "localField": "user_id",
            "foreignField": "code",
            "as": "users"
        }}

        books_lookup = {'$lookup': {
            "from": "users",
            "localField": "user_id",
            "foreignField": "code",
            "as": "users"
        }}

        # build query
        querry_command = [
            filter_aggregation,
            user_lookup
        ]

        voucher_result_dict = list(self.voucher_collection.aggregate(querry_command))

        if not voucher_result_dict:
            return None
        voucher_result_dict = self._dict_to_voucher_detail_result(voucher_result_dict[0])
        return voucher_result_dict

    def _dict_to_voucher_detail_result(self, voucher_dict: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(voucher_dict)
        dict_object_id['users'] = dict_object_id.get('users')[0]
        result = VoucherDetailOutDB(**dict_object_id)
        for i in range(len(result.books_borrowed)):
            book_data = self.book_repo.get_detail_book_repo(result.books_borrowed[i])
            result.books_borrowed[i] = book_data

        return result

    def update_voucher_repo(self, voucher_id: str, data_update: VoucherUpdate):
        data_update = data_update.dict()
        data_update['modified_time'] = datetime_utils.get_string_datetime_now()
        voucher_id = voucher_id.strip()
        _update_result = self.voucher_collection.update_one({'voucher_id': voucher_id},
                                                          {'$set': data_update})
        if _update_result and _update_result.modified_count == 1:
            book_result_dict = self.get_detail_voucher_repo(voucher_id=voucher_id)
            return book_result_dict
        return None

    def delete_voucher_repo(self, voucher_id: str):
        voucher_id = voucher_id.strip()
        _delete_result = self.voucher_collection.update_one({'voucher_id': voucher_id},
                                                            {'$set': {'is_active': False}})
        if _delete_result and _delete_result.modified_count == 1:
            return True
        return False

    def update_status_voucher_repo(self, voucher_id: str, status_update: str):
        modified_time = datetime_utils.get_string_datetime_now()
        voucher_id = voucher_id.strip()
        _update_result = self.voucher_collection.update_one({'voucher_id': voucher_id},
                                                            {'$set': {
                                                                'modified_time': modified_time,
                                                                'status_voucher': status_update
                                                            }})
        if _update_result and _update_result.modified_count == 1:
            book_result_dict = self.get_detail_voucher_repo(voucher_id=voucher_id)
            return book_result_dict
        return None