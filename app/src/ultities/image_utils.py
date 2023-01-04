import io
import os

import aiofiles
from PIL import Image
from fastapi import File, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from app.src.ultities import datetime_utils


async def create_upload_file( path: str, file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join(path, 'storage\\')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{str(datetime_utils.get_timestamp_now())}_{file.filename}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)
    path_result = f'\storage\{file_name}'
    return path_result
