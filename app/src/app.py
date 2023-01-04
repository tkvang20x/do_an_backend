import os

from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.controller import book_controller, login_controller, user_controller, image_controller

BASEDIR = os.path.dirname(__file__)
# app.mount("/controller/storage", StaticFiles(directory=BASEDIR + "/controller/storage"), name="storage")


app.include_router(
    login_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - LOGIN API"]
)

app.include_router(
    book_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - BOOK API"]
)

app.include_router(
    user_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN-USER RESOURCES] - USER API"]
)

app.include_router(
    image_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN-USER RESOURCES] - IMAGE API"]
)
