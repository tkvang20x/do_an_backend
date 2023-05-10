import asyncio
import os
import time

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import schedule
from app.src.base.base_api import app
from app.src.controller import books_controller, login_controller, user_controller, image_controller, book_controller, \
    group_books_controller, book_voucher_controller, manager_controller, change_password_controller
from app.src.service.book_voucher_service import BookVoucherService

voucher_service = BookVoucherService()

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

app.include_router(
    change_password_controller.router,
    prefix=f'/do-an/v1',
    tags=["[ADMIN RESOURCES] - CHANGE PASSWORD API"]
)


def job_function():
    # Do something here
    voucher_service.get_all_voucher_before_date_now()


async def run_jobs():
    schedule.every().day.at("00:00:01").do(job_function)
    # job_function()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_jobs())

