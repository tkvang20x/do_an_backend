import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.book_model import DetailBook
from app.src.ultities import collection_utils, mongo_utils

BOOK_COLLECTION = "book"


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
            # init data
            total = 0
            total_page = 0
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
        except Exception as e:
            logging.error(f"Get List OCR Engine error -- Caused by '{e.__str__()}")
            return None

    def _dict_to_list_book_result(self, dict_book: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(dict_book)
        result = DetailBook(**dict_object_id)
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