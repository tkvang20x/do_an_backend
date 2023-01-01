import io
import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, APIRouter, Response
import uuid
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from PIL import Image
import PIL
from app.src.base.base_service import BaseRoute

router = APIRouter(
    route_class=BaseRoute
)

db = []


@router.post("/images")
async def create_upload_file(file: UploadFile = File(...)):
    # file.filename = f"{uuid.uuid4()}.jpg"

    contents = await file.read()
    data_image = io.BytesIO(contents)

    path = r"F:\do_an_backend\app\src\storage"
    image = Image.open(data_image)
    image.save(path + "\\" + file.filename)

    path_result = path + "\\" + file.filename
    path_result = path_result.replace("\\" , "/")
    data = StreamingResponse(io.BytesIO(contents), media_type="image/png")

    return {"path" : path_result}


@router.get("/images")
async def read_random_file():
    file = {
        "filename": "kien.png",
        "content_type": "image/png",
        "file": {},
        "headers": {
            "content-disposition": "form-data; name=\"file\"; filename=\"kien.png\"",
            "content-type": "image/png"
        }
    }

    content = file.read()

    return StreamingResponse(io.BytesIO(content), media_type="image/png")
