import datetime
import uuid
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

"""Base Response Object Configs"""


class ResponseObject:

    def __init__(self):
        super().__init__()
        self.data = None
        self.message = ""
        self.code = ""
        self.links = ""
        self.relationships = ""
        self.timestame = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def success(self, data=None, code="0", message=None, links=None, relationships=None):
        self.data = data
        self.message = message
        self.code = code
        self.links = links
        self.relationships = relationships
        return self

    def error(self, status_code=400, data=None, message="error", code="1", links=None, relationships=None):
        self.message = message
        self.code = code
        self.data = data
        self.links = links
        self.relationships = relationships
        return JSONResponse(status_code=status_code, content=jsonable_encoder(self))


class ResponseCommon:
    """
           API Response Model
        """

    def __init__(self):
        self.common_message = {"client_message_id": str(uuid.uuid4()),
                               "data": None,
                               "status": None,
                               "error": None,
                               "path": None}

    def data(self, result,
             status: str,
             path: str = None):
        self.common_message['data'] = result
        self.common_message['status'] = status
        self.common_message['error'] = "OK"
        self.common_message['path'] = path
        return self.common_message

    def dataResource(self, result,
             status: str,
             path: str = None):
        self.common_message['data'] = {"result": result}
        self.common_message['status'] = status
        self.common_message['error'] = "OK"
        self.common_message['path'] = path
        return self.common_message

    def success(self, result,
                status: str,
                path: str = None):
        # if  result response is None -> default value
        if result is None:
            result = {}
        # if result response not dict ->  convert to dict
        # if not isinstance(result,dict):
        #     result = result.__dict__
        # if  result response not inside 'result'  -> wrap to 'result' object [apply for Object response]
        # if not result.get('result') and not result.get('result') == []:
        self.common_message['data'] = result
        self.common_message['status'] = status
        self.common_message['error'] = "OK"
        self.common_message['path'] = path
        return self.common_message

    def error(self, status: str,
              error_message: str,
              path: str = None,
              soa_error_code: str = None,
              soa_error_desc: str = None):
        self.common_message['status'] = status
        self.common_message['error'] = error_message
        self.common_message['path'] = path
        return self.common_message


class ResponseException:
    """
        Response Exception
    """

    def response(self, status: int,
                 error_message: str,
                 path: str):
        error_content = {"client_message_id": str(uuid.uuid4()),
                         "data": None,
                         "status": status,
                         "error": error_message,
                         "path": path,}
        json_response = JSONResponse(status_code=status, content=jsonable_encoder(error_content))
        _headers = json_response.headers.mutablecopy()
        _headers.update({"Access-Control-Allow-Origin": "*"})

        return JSONResponse(status_code=status, content=jsonable_encoder(error_content), headers=_headers)
