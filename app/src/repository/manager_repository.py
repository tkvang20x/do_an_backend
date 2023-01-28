import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.base import base_model
from app.src.model.manager_model import ListManager, CreateManager, DetailManager, UpdateManager
from app.src.ultities import mongo_utils, collection_utils, datetime_utils

MANAGER_COLLECTION = "managers"


class ManagerRepository(MongoBaseRepo):
    def __init__(self):
        super(ManagerRepository, self).__init__(MANAGER_COLLECTION)
        self.manager_collection = self.collection
        self._record_status_active = {'is_active': True}

    def get_list_manager_repo(self, page: int,
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

            list_user_result_dict = list(
                self.manager_collection.find(filter_condition).sort([(order_by, order)]).skip(skip).limit(size))
            if collection_utils.list_none_or_empty(list_user_result_dict):
                list_users = []
            else:
                list_users = [self._dict_to_list_manager_result(user) for user in
                              list_user_result_dict]

            # count total
            total = self.manager_collection.count_documents(filter_condition)
            # calculate total page
            if not total or total == 0:
                total_page = 0
            else:
                total_page = ((total + size - 1) // size)
            result_pagnition = base_model.coor_response(response_data=list_users,
                                                        page=page,
                                                        limit=size,
                                                        sort_by=order_by,
                                                        sort=order,
                                                        total_records=total,
                                                        total_page=total_page)

            return result_pagnition
        except Exception as e:
            logging.error(f"Get List User error -- Caused by '{e.__str__()}")
            return None

    def create_manager_repo(self, data_create: DetailManager):
        try:
            data_create = data_create.dict()
            if 'id' in data_create:
                del data_create['id']

            self.manager_collection.insert_one(data_create)
            book_result_dict = self._dict_to_create_manager_result(data_create)
            return book_result_dict
        except Exception as e:
            logging.error(f"Create user to db error! -- Caused by '{e.__str__()}")
            return None

    def _dict_to_create_manager_result(self, data_dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(data_dict)
        result = DetailManager(**dict_object_id)
        result.id = dict_object_id.get('_id')
        return result

    def _dict_to_list_manager_result(self, user: dict):
        user_convert_string = mongo_utils.convert_object_id_to_string(user)
        result_user = ListManager(**user_convert_string)
        return result_user

    def get_detail_manager_repo(self, code: str):
        code = code.strip()
        user_result = self.manager_collection.find_one({"code": code, 'is_active': True})
        if not user_result:
            return None
        user_result_dict = self._dict_to_create_manager_result(user_result)
        return user_result_dict

    def check_user_name_manager(self, user_name: str):
        user_name = user_name.strip()
        user_result = self.manager_collection.find_one({"user_name": user_name, 'is_active': True})
        if not user_result:
            return False
        user_result_dict = self._dict_to_create_manager_result(user_result)
        return True

    def update_manager_repo(self, code: str, data_update: UpdateManager):
        data_update = data_update.dict()
        data_update['modified_time'] = datetime_utils.get_string_datetime_now()
        code = code.strip()
        _update_result = self.manager_collection.update_one({'code': code},
                                                         {'$set': data_update})
        if _update_result and _update_result.modified_count == 1:
            book_result_dict = self.get_detail_manager_repo(code=code)
            return book_result_dict
        return None

    def delete_manager_repo(self, code: str):
        delete_result = self.manager_collection.update_one({'code': code.strip()},
                                                        {'$set': {'is_active': False}})
        if delete_result and delete_result.modified_count == 1:
            return True
        return False

    def update_avatar_manager_repo(self, code: str, path_avatar: str):
        code = code.strip()
        _update_result = self.manager_collection.update_one({'code': code},
                                                         {'$set': {'avatar': path_avatar}})
        if _update_result and _update_result.modified_count == 1:
            return True
        return False