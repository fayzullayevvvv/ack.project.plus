from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.models import RoleCode


class AdminUpdateUser(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=5)
    last_name: Optional[str] = Field(default=None, min_length=5)
    username: Optional[str] = Field(default=None, min_length=5)
    email: Optional[EmailStr] = None
    role: Optional[RoleCode] = None
    password: Optional[str] = Field(default=None, min_length=8)
    confirm_password: Optional[str] = Field(default=None, min_length=8)

    @field_validator("first_name", "username")
    @classmethod
    def validate_not_empty(cls, value: Optional[str]):
        if value is not None and not value.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return value
    
    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password or self.confirm_password:
            if not self.password or not self.confirm_password:
                raise ValueError("Both password and confirm_password are required")

            if self.password != self.confirm_password:
                raise ValueError("Passwords do not match")

        return self