import io
from random import randint
import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, APIRouter, Response
import uuid
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse

from app.src.base.base_service import BaseRoute

router = APIRouter(
    route_class=BaseRoute
)

db = []


@router.post("/images")
async def create_upload_file(file: UploadFile = File(...)):
    # file.filename = f"{uuid.uuid4()}.jpg"

    contents = await file.read()
    print(type(file))
    data = StreamingResponse(io.BytesIO(contents), media_type="image/png")
    return {"result" : file}


@router.get("/images")
async def read_random_file():

    file = {
        "filename": "319407639_1531551200603473_1387888714467454381_n.png",
        "content_type": "image/png",
        "file": {},
        "headers": {
            "content-disposition": "form-data; name=\"file\"; filename=\"319407639_1531551200603473_1387888714467454381_n.png\"",
            "content-type": "image/png"
        }
    }

    content = file.read()

    return StreamingResponse(io.BytesIO(content), media_type="image/png")
