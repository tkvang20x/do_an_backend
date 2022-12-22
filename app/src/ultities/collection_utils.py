def list_none_or_empty(list_object):
    """ Check list none or empty
                    return: True | False
                """
    return True if (list_object is None or len(list_object) == 0) else False
