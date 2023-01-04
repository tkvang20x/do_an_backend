import io
import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, APIRouter, Request, HTTPException
import uuid

from starlette import status
from starlette.staticfiles import StaticFiles

from app.src.base.base_api import app
from app.src.base.base_model import ResponseCommon
from app.src.base.base_service import BaseRoute
from fastapi import FastAPI

from app.src.ultities import datetime_utils


router = APIRouter(
    route_class=BaseRoute
)

BASEDIR = os.path.dirname(__file__)
app.mount("/storage", StaticFiles(directory=BASEDIR + "/storage"), name="storage")

@router.post("/images")
async def create_upload_file(request: Request,file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join(BASEDIR, 'storage\\')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{str(datetime_utils.get_timestamp_now())}_{file.filename}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)
    path_result = f'storage\\{file_name}'
    path_result = path_result.replace("\\", "/")

    return ResponseCommon().success(result=path_result, status=status.HTTP_201_CREATED, path=request.url.path)



