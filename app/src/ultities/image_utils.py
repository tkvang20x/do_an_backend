import io

from PIL import Image
from fastapi import File
from starlette.responses import StreamingResponse


async def create_upload_file(file: File):
    # file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    data_image = io.BytesIO(contents)

    path = r"F:\do_an_backend\app\src\storage"
    image = Image.open(data_image)
    image.save(path + "\\" + file.filename)

    path_result = path + "\\" + file.filename
    path_result = path_result.replace("\\", "/")
    # data = StreamingResponse(io.BytesIO(contents), media_type="image/png")
    return path_result
