import logging

import decouple
import motor.motor_asyncio
from pymongo import MongoClient


def get_collection(collection_name, is_async):
    try:
        if is_async:
            mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
        else:
            mongo_client = MongoClient("mongodb://localhost:27017/")
        db_connection = mongo_client["do_an"]
        return db_connection.get_collection(collection_name)
    except Exception as ee:
        logging.error(
            f"Can't connect to Mongo server  - db name "
            f"and get collection collection_name error. - Caused by:  [{ee.__str__()}]")


class MongoBaseRepo:
    def __init__(self, collection_name, is_async=False):
        self.collection = get_collection(collection_name, is_async)


class MongoBaseRepoAsync:
    def __init__(self, collection_name, is_async=True):
        self.collection_async = get_collection(collection_name, is_async)
