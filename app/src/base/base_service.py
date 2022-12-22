import ast
import json
import logging
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute


async def _request_data_handle(request: Request):
    request_data = {"request_headers": request.headers.__dict__}
    str_message = None
    dict_message = None
    # LOG Request
    try:
        # check if request body is bytes, don't show contents
        str_message = await request.body()
        if isinstance(str_message, bytes):
            dict_message = {'file-attachments': "Bytes data"}
        else:
            dict_message = ast.literal_eval(str_message.decode(encoding="utf-8"))
    except ValueError:
        dict_message = json.loads(str_message.decode(encoding="utf-8"))
    except Exception as e:
        logging.debug(f'Base route: [{e.__str__()}]')
    request_data['request_body'] = dict_message
    if request.query_params or request.path_params:
        request_data['query_params'] = request.query_params
        request_data['path_params'] = request.path_params
    logging.info(request_data)


class BaseRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # log request data
            await _request_data_handle(request=request)
            # LOG response
            # log request data
            response_data = {}
            response: Response = await original_route_handler(request)
            try:
                response_value = response.body
                if isinstance(response_value, bytes):
                    response_data = {'file_content_bytes': "Bytes data"}
                else:
                    response_data = {"response_data": response.body.__str__()}
            except ValueError:
                response_data = {"response_data": response.body.__str__()}
            except Exception as e:
                logging.debug(f'Base route: [{e.__str__()}]')
            logging.info(response_data)
            return response

        return custom_route_handler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
