import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.book_model import DetailBook, ListBook, UpdateBook, UpdateUserBook
from app.src.ultities import collection_utils, mongo_utils, datetime_utils

BOOK_COLLECTION = "book"
SYNTAS_LOOKUP = "$lookup"


class BookRepository(MongoBaseRepo):
    def __init__(self):
        super(BookRepository, self).__init__(BOOK_COLLECTION)
        self.book_collection = self.collection
        self._record_status_active = {'is_active': True}

    def get_list_book_repo(self, page: int,
                           size: int,
                           order_by: str,
                           order: int,
                           filter_condition: dict):
        try:
            if size > 0:
                skip = (page - 1) * size
                # build filter condition
                # Get list ocr_engine by condition
                filter_condition.update(self._record_status_active)

                list_book_result_dict = list(
                    self.book_collection.find(filter_condition).sort([(order_by, order)]).skip(skip).limit(size))
                if collection_utils.list_none_or_empty(list_book_result_dict):
                    list_book = []
                else:
                    list_book = [self._dict_to_list_book_result(book) for book in
                                 list_book_result_dict]

                # count total
                total = self.book_collection.count_documents(filter_condition)
                # calculate total page
                if not total or total == 0:
                    total_page = 0
                else:
                    total_page = ((total + size - 1) // size)
                result_pagnition = base_model.coor_response(response_data=list_book,
                                                            page=page,
                                                            limit=size,
                                                            sort_by=order_by,
                                                            sort=order,
                                                            total_records=total,
                                                            total_page=total_page)

                return result_pagnition
            else:
                filter_condition.update(self._record_status_active)

                list_book_result_dict = list(
                    self.book_collection.find(filter_condition).sort([(order_by, order)]))
                if collection_utils.list_none_or_empty(list_book_result_dict):
                    list_book = []
                else:
                    list_book = [self._dict_to_list_book_result(book) for book in
                                 list_book_result_dict]
                result_pagnition = base_model.coor_response(response_data=list_book,
                                                            page=page,
                                                            limit=0,
                                                            sort_by=order_by,
                                                            sort=order,
                                                            total_records=len(list_book),
                                                            total_page=1)
                return result_pagnition
        except Exception as e:
            logging.error(f"Get List Book error -- Caused by '{e.__str__()}")
            return None

    def get_all_book_repo(self, code_books: str, status_borrow: str):
        try:
            # init data
            total = 0
            filter_condition = {}
            # build filter condition
            # Get list ocr_engine by condition
            filter_condition.update(self._record_status_active)
            if status_borrow != "":
                filter_condition.update({"code_books": code_books,"status_borrow":status_borrow})
            else:
                filter_condition.update({"code_books": code_books})
            # count total
            total = self.book_collection.count_documents(filter_condition)
            return total
        except Exception as e:
            logging.error(f"Get Size Book error -- Caused by '{e.__str__()}")
            return None

    def _dict_to_list_book_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        result = ListBook(**dict_object_id)
        return result

    def create_book_repo(self, data: DetailBook):
        try:
            create_data = data.dict()
            if 'id' in create_data:
                del create_data['id']

            self.book_collection.insert_one(create_data)
            book_result_dict = self._dict_to_list_book_result(create_data)
            return book_result_dict
        except Exception as e:
            logging.error(f"Create book error! -- Caused by '{e.__str__()}")
            return None

    def get_detail_book_repo(self, code_id: str):
        code_id = code_id.strip()
        book_match_id = {"$match": {"code_id": code_id, 'is_active': True}}
        books_lookup = {SYNTAS_LOOKUP: {
            "from": "books",
            "localField": "code_books",
            "foreignField": "code",
            "as": "books"
        }}

        groups_lookup = {SYNTAS_LOOKUP: {
            "from": "groups",
            "localField": "books.group_code",
            "foreignField": "group_code",
            "as": "groups"
        }}

        # build query
        querry_command = [
            book_match_id,
            books_lookup,
            groups_lookup
        ]

        # get full result dict
        result_dict_list = list(self.book_collection.aggregate(querry_command))
        if not result_dict_list:
            return None
        book_result_dict = self._dict_to_detail_book_result(result_dict_list[0])
        return book_result_dict

    def _dict_to_detail_book_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        dict_object_id['books'] = dict_object_id.get('books')[0]
        if len(dict_object_id['groups']) > 0:
            dict_object_id['groups'] = dict_object_id.get('groups')[0]
        result = DetailBook(**dict_object_id)
        result.id = dict_object_id.get('_id')
        total_books_ready = self.get_all_book_repo(code_books=result.code_books, status_borrow="READY")
        result.books.total_books_ready = total_books_ready
        return result

    def update_book_repo(self, code_id: str, data_update: UpdateBook):
        data_update = data_update.dict()
        data_update['modified_time'] = datetime_utils.get_string_datetime_now()
        # code_id = code_id.strip()
        _update_result = self.book_collection.update_one({'code_id': code_id},
                                                         {'$set': data_update})
        if _update_result and _update_result.modified_count == 1:
            book_result_dict = self.get_detail_book_repo(code_id=code_id)
            return book_result_dict
        return None

    def delete_book_repo(self, code_id: str):
        delete_result = self.book_collection.update_one({'code_id': code_id.strip()},
                                                        {'$set': {'is_active': False}})
        if delete_result and delete_result.modified_count == 1:
            return True
        return False

    def get_list_id_book_repo(self, size: int, filter_condition: dict):
        try:
            # Get list ocr_engine by condition
            filter_condition.update(self._record_status_active)

            filter_condition_new = {'$match': filter_condition}
            size_aggregation = {'$limit': size}

            books_lookup = {'$lookup': {
                "from": "books",
                "localField": "code_books",
                "foreignField": "code",
                "as": "books"
            }}

            # build query
            querry_command = [
                filter_condition_new,
                size_aggregation,
                books_lookup
            ]

            list_id_book_result_dict = list(self.book_collection.aggregate(querry_command))

            if collection_utils.list_none_or_empty(list_id_book_result_dict):
                list_id_book = []
            else:
                list_id_book = [self._dict_to_id_book(book) for book in list_id_book_result_dict]

            return list_id_book
        except Exception as e:
            logging.error(f"Get List Book error -- Caused by '{e.__str__()}")
            return None


    def _dict_to_id_book(self, book: dict):
        convert_dict = {
            'code_id': book.get('code_id'),
            'name_books': book.get('books')[0].get('name'),
            'author':book.get('books')[0].get('author'),
            'avatar': book.get('books')[0].get('avatar')
        }
        return convert_dict

    def update_user_book_repo(self, code_id: str, data_update: UpdateUserBook):
        data_update = data_update.dict()
        data_update['modified_time'] = datetime_utils.get_string_datetime_now()
        code_id = code_id.strip()
        _update_result = self.book_collection.update_one({'code_id': code_id},
                                                         {'$set': data_update})
        if _update_result and _update_result.modified_count == 1:
            return True
        return False