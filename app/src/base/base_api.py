from fastapi import FastAPI

from app.src.base.base_exception import error_handle_business

app = FastAPI(title='DO AN SERVICE',
              description='Do an service')

app.add_exception_handler(Exception, error_handle_business)


