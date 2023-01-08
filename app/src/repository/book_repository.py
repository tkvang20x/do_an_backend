import logging


from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.book_model import DetailBook, ListBook
from app.src.ultities import collection_utils, mongo_utils

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

    def get_all_book_repo(self, code_books: str):
        try:
            # init data
            total = 0
            filter_condition = {}
            # build filter condition
            # Get list ocr_engine by condition
            filter_condition.update(self._record_status_active)
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

        # build query
        querry_command = [
            book_match_id,
            books_lookup,
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
        result = DetailBook(**dict_object_id)
        result.id = dict_object_id.get('_id')
        return result