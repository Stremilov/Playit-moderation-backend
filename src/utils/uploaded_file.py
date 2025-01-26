# загрузка медиа логика в сервисе
import uuid

from fastapi import UploadFile, HTTPException, status

from core.config import UPLOAD_FOLDER


async def upload_file(uploaded_file: UploadFile):
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
    file_path = UPLOAD_FOLDER / unique_filename

    try:
        with open(file_path, "wb") as f:
            content = await uploaded_file.read()
            f.write(content)
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
