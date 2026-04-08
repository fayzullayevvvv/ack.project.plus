from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models import RoleCode


class AdminUpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleCode] = None
    password: Optional[str] = None
