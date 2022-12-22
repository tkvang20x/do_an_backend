from fastapi import FastAPI

from app.src.base.base_exception import error_handle_business

app = FastAPI(title='OCR Coordinator Admin Microservice',
              description='A part of OCR Center')

app.add_exception_handler(Exception, error_handle_business)


