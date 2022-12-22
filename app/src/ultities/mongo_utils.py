import re
from typing import List

from bson import ObjectId
from bson.errors import InvalidId

from app.src.ultities import string_utils, collection_utils


def convert_object_id_to_string(obj):
    """
        Convert object id to string
    """
    for key in obj.keys():
        if isinstance(obj[key], dict):
            obj[key] = convert_object_id_to_string(obj[key])
        elif isinstance(obj[key], list):
            obj[key] = convert_object_id_to_string_array(obj[key])
        elif isinstance(obj[key], ObjectId):
            obj[key] = str(obj[key])
    return obj


def convert_object_id_to_string_array(array):
    """
        Convert object id to string in array
    """
    res = []
    for item in array:
        if isinstance(item, dict):
            res.append(convert_object_id_to_string(item))
        elif isinstance(item, list):
            res.append(convert_object_id_to_string_array(item))
        elif isinstance(item, ObjectId):
            res.append(str(item))
        else:
            res.append(item)
    return res


def build_filter_like_keyword(keyword: str):
    """
        Build keyword for search LIKE for MongoDB

    :param keyword:
    :return:
    """
    if string_utils.string_none_or_empty(keyword):
        return ""
    return {'$regex': f'.*{format(re.escape(keyword))}.*', '$options': 'i'}

def list_string_to_object_id(str_ids: List[str]):
    list_object_ids = []
    if collection_utils.list_none_or_empty(str_ids):
        return []
    for str_id in str_ids:
        list_object_ids.append(ObjectId(str_id))
    return list_object_ids


def string_to_object_id(string_id: str):
    """
        Try convert string to Object ID
    :param string_id:
    :return:
    """
    try:
        object_id_convert = ObjectId(string_id)
        return object_id_convert
    except InvalidId:
        return None
    except Exception:
        return None
