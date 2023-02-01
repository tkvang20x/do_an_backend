import os

from starlette.middleware.cors import CORSMiddleware

from app.src.base.base_api import app
from app.src.controller import books_controller, login_controller, user_controller, image_controller, book_controller, \
    group_books_controller, book_voucher_controller, manager_controller

BASEDIR = os.path.dirname(__file__)
# app.mount("/controller/storage", StaticFiles(directory=BASEDIR + "/controller/storage"), name="storage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    login_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - LOGIN API"]
)

app.include_router(
    books_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - BOOKS API"]
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

app.include_router(
    book_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - BOOK API"]
)

app.include_router(
    group_books_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - GROUP API"]
)

app.include_router(
    book_voucher_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - VOUCHER API"]
)


app.include_router(
    manager_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - MANAGER API"]
)
