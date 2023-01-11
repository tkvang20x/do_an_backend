import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.group_books_model import GroupBooks
from app.src.ultities import mongo_utils, collection_utils

GROUP_COLLECTION = "groups"


class GroupBooksRepository(MongoBaseRepo):
    def __init__(self):
        super(GroupBooksRepository, self).__init__(GROUP_COLLECTION)
        self.group_collection = self.collection
        self._record_status_active = {'is_active': True}

    def create_group_repo(self, data: GroupBooks):
        try:
            create_data = data.dict()
            if 'id' in create_data:
                del create_data['id']

            self.group_collection.insert_one(create_data)
            group_result_dict = self._dict_to_group_result(create_data)
            return group_result_dict
        except Exception as e:
            logging.error(f"Create group error! -- Caused by '{e.__str__()}")
            return None

    def _dict_to_group_result(self, data_group: dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(data_group)
        result = GroupBooks(**dict_object_id)
        return result

    def get_list_group_repo(self):
        try:
            # init data
            total = 0
            filter_condition = {}
            # build filter condition
            # Get list ocr_engine by condition
            filter_condition.update(self._record_status_active)
            list_group_result_dict = list(
                self.group_collection.find(filter_condition))
            if collection_utils.list_none_or_empty(list_group_result_dict):
                list_book = []
            else:
                list_book = [self._dict_to_group_result(book) for book in
                             list_group_result_dict]

            # count total
            total = self.group_collection.count_documents(filter_condition)
            # calculate total page
            result_pagnition = base_model.coor_response(response_data=list_book,
                                                        total_records=total)

            return result_pagnition
        except Exception as e:
            logging.error(f"Get Size Book error -- Caused by '{e.__str__()}")
            return None