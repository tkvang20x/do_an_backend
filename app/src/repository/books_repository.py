import logging
from builtins import filter

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.books_model import CreateDataBook, DetailBooks, ListBook, UpdateBookData, UpdateBookDataFormService
from app.src.repository.book_repository import BookRepository
from app.src.ultities import mongo_utils, collection_utils, datetime_utils

BOOKS_COLLECTION = "books"

SYNTAS_LOOKUP = "$lookup"
SYNTAS_MATCH = "$match"
GROUPS_DELETED = 'GROUPS_DELETED'


class BooksRepository(MongoBaseRepo):
    def __init__(self):
        super(BooksRepository, self).__init__(BOOKS_COLLECTION)
        self.books_collection = self.collection
        self._record_status_active = {'is_active': True}
        self.book_repository = BookRepository()

    def create_book_repo(self, data: DetailBooks):
        try:

            create_data = data.dict()
            if 'id' in create_data:
                del create_data['id']

            self.books_collection.insert_one(create_data)
            book_result_dict = self._dict_to_create_book_result(create_data)
            return book_result_dict
        except Exception as e:
            logging.error(f"Create book error! -- Caused by '{e.__str__()}")
            return None

    def _dict_to_create_book_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        if dict_object_id['groups']:
            dict_object_id['groups'] = dict_object_id.get('groups')[0]
        result = DetailBooks(**dict_object_id)
        result.id = dict_object_id.get('_id')
        return result

    def get_list_book_repo(self, page: int,
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
            filter_condition_count_document = {}
            filter_condition_count_document.update(self._record_status_active)
            filter_condition_count_document.update(filter_condition)
            # if group_code is not None:
            #     filter_aggregation = {'$match': {'is_active': True,'group_code': group_code}}
            #     filter_condition_count_document.update({'group_code': group_code})
            # else:
            #     filter_aggregation = {'$match': {'is_active': True}}
            sort_aggregation = {'$sort': {f'{order_by}': order}}
            skip_aggregation = {'$skip': skip}
            size_aggregation = {'$limit': size}
            filter_condition = {'$match': filter_condition_count_document}

            group_lookup = {'$lookup': {
                "from": "groups",
                "localField": "group_code",
                "foreignField": "group_code",
                "as": "groups"
            }}

            # build query
            querry_command = [
                # filter_aggregation,
                filter_condition,
                sort_aggregation,
                skip_aggregation,
                size_aggregation,
                group_lookup
            ]

            # get full result dict
            list_books_result_dict = list(self.books_collection.aggregate(querry_command))


            # list_books_result_dict = list(
            #     self.books_collection.find(filter_condition).sort([(order_by, order)]).skip(skip).limit(size))
            if collection_utils.list_none_or_empty(list_books_result_dict):
                list_books = []
            else:
                list_books = [self._dict_to_list_book_result(book) for book in
                              list_books_result_dict]

            # count total
            total = self.books_collection.count_documents(filter_condition_count_document)
            # calculate total page
            if not total or total == 0:
                total_page = 0
            else:
                total_page = ((total + size - 1) // size)
            result_pagnition = base_model.coor_response(response_data=list_books,
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

    def _dict_to_list_book_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        if len(dict_object_id.get('groups')) > 0:
            dict_object_id['groups'] = dict_object_id.get('groups')[0]
        else:
            dict_object_id['groups'] = None
        result = ListBook(**dict_object_id)
        result.total_books = self.book_repository.get_all_book_repo(code_books=result.code)
        return result

    def get_detail_book_repo(self, code: str):
        code = code.strip()
        filter_aggregation = {'$match': {'is_active': True, 'code': code}}
        group_lookup = {'$lookup': {
            "from": "groups",
            "localField": "group_code",
            "foreignField": "group_code",
            "as": "groups"
        }}
        # build query
        querry_command = [
            filter_aggregation,
            group_lookup
        ]

        books_result_dict = list(self.books_collection.aggregate(querry_command))

        # book_result = self.books_collection.find_one({"code": code, 'is_active': True})
        if not books_result_dict:
            return None
        book_result_dict = self._dict_to_create_book_result(books_result_dict[0])
        return book_result_dict

    def update_book_repo(self, code: str, data_update: UpdateBookDataFormService):
        data_update = data_update.dict()
        data_update['modified_time'] = datetime_utils.get_string_datetime_now()
        code = code.strip()
        _update_result = self.books_collection.update_one({'code': code},
                                                          {'$set': data_update})
        if _update_result and _update_result.modified_count == 1:
            book_result_dict = self.get_detail_book_repo(code=code)
            return book_result_dict
        return None

    def delete_book_repo(self, code: str):
        delete_result = self.books_collection.update_one({'code': code.strip()},
                                                         {'$set': {'is_active': False}})
        if delete_result and delete_result.modified_count == 1:
            return True
        return False

    def update_avatar_books_repo(self, code: str, path_avatar: str):
        code = code.strip()
        _update_result = self.books_collection.update_one({'code': code},
                                                          {'$set': {'avatar': path_avatar}})
        if _update_result and _update_result.modified_count == 1:
            return True
        return False

    def update_books_when_delete_groups(self, group_code: str):
        group_code = group_code.strip()
        _update_result = self.books_collection.update_many({'group_code': group_code},
                                                           {'$set': {'group_code': GROUPS_DELETED}})
        if _update_result:
            return True
        return False