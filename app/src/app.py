from app.src.base.base_api import app
from app.src.controller import book_controller, login_controller, upload_image_controller

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
    upload_image_controller.router,
    prefix= f'/do-an/v1',
    tags = ["[ADMIN RESOURCES] - IMAGE API"]
)