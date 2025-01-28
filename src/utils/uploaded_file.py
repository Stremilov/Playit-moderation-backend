# загрузка медиа логика в сервисе
# TODO сделай не только загрузку но и удаление файлов
import uuid

from fastapi import UploadFile

from core.config import UPLOAD_FOLDER
from utils.Exception import handle_http_exceptions


@handle_http_exceptions
async def upload_file(uploaded_file: UploadFile):
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
    file_path = UPLOAD_FOLDER / unique_filename
    with open(file_path, "wb") as f:
        content = await uploaded_file.read()
        f.write(content)
    return str(file_path)
