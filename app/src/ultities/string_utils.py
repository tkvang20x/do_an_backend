import logging
import re
import urllib.parse as parser
from ast import literal_eval

from bson import ObjectId
from bson.errors import InvalidId



def string_none_or_empty(str_value: str) -> bool:
    """ Check string none or empty
                return: True | False
            """
    return True if not str_value or len(str_value) == 0 else False


def convert_string_to_dict(str_value: str):
    """
        Convert string to dict
    """
    try:
        dict_value = literal_eval(str_value)
        return dict_value
    except ValueError as e:
        logging.info(f"[string_utils] Convert string to dict error -- caused by: {e.__str__()}")
        return None


def parse_string_url(string_url: str):
    """
        Parse string URL
        example:
          - in: id%253D184ff84d27c3613d%26quality%3Dmedium
          - out: id=184ff84d27c3613d&quality=medium
    """
    try:
        return parser.unquote(string_url)
    except ValueError as e:
        logging.info(f"[string_utils] Parse string url error -- caused by: {e.__str__()}")
        return None


def convert_string_to_bson_object_id(str_value: str):
    """
        Convert string to dict
    """
    try:
        object_id = ObjectId(str_value)
        return object_id
    except InvalidId as e:
        logging.info(f"[string_utils] Convert string to Bson Object ID error -- caused by: {e.__str__()}")
        return None


def check_special_character_in_string(string: str) -> bool:
    # find character not valid
    x = re.search(r"([^a-zA-Z0-9_.])", string)
    # if exist charactor not valid:
    if x:
        return True
    else:
        return False


# def check_string_is_image_name(string: str) -> bool:
#     extension = get_file_extension_from_name(file_name=string)
#     if extension is not None and extension in ['jpg', 'jpeg', 'png', 'tif', 'tiff']:
#         return True
#     else:
#         return False


def format_date(str_replace):
    str_replace = str_replace.replace('.', '')
    str_replace = str_replace.replace(':', '')
    try:
        str_date = re.findall(r'\d+', str_replace)
        if str_date:
            year = [s for s in str_date][-1]
            month = [s for s in str_date if s.isdigit() and int(s) < 13][-1]
            if len(month) == 1:
                month = '0' + str(month)
            day = [s for s in str_date if s.isdigit() and int(s) < 32][0]
            return "{day}/{month}/{year}".format(day=day, month=month, year=year)
        return None
    except Exception as e:
        logging.info(f"[string_utils] Format date error -- caused by: {e.__str__()}")
        return None
