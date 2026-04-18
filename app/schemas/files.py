from pydantic import BaseModel

from app.models import File, FileType


class UploadResponse(BaseModel):
    file_id: int
    attachment_id: int
    original_name: str
    stored_name: str
    file_type: FileType
    size: int


class FileResponse(BaseModel):
    path: str
    filename: str
    media_type: str
    headers: None|dict


class SignedUrlResponse(BaseModel):
    url: str
    expires_in: int