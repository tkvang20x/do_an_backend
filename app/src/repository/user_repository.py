import logging

from app.src.base.base_repository import MongoBaseRepo
from app.src.model.user_model import CreateUser, DetailUser
from app.src.ultities import mongo_utils

USER_COLLECTION = "users"

class UserRepository(MongoBaseRepo):
    def __init__(self):
        super(UserRepository, self).__init__(USER_COLLECTION)
        self.user_collection = self.collection
        self._record_status_active = {'is_active': True}

    def create_user_repo(self, data_create: CreateUser):
        try:
            data_create = data_create.dict()
            if 'id' in data_create:
                del data_create['id']

            self.user_collection.insert_one(data_create)
            book_result_dict = self._dict_to_create_user_result(data_create)
            return book_result_dict
        except Exception as e:
            logging.error(f"Create user to db error! -- Caused by '{e.__str__()}")
            return None

    def _dict_to_create_user_result(self, data_dict):
        dict_object_id = mongo_utils.convert_object_id_to_string(data_dict)
        result = DetailUser(**dict_object_id)
        result.id = dict_object_id.get('_id')
        return result