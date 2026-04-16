from typing import Optional

from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile


class UserProfile(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    full_name: Optional[str]
    phone: Optional[str]
    avatar_file_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UpdateProfile(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_file_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Avatar(BaseModel):
    photo: UploadFile
