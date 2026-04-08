from enum import Enum

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WORKER = "worker"


class CreateUser(BaseModel):
    full_name: str = Field(min_length=5)
    username: str = Field(min_length=5)
    email: EmailStr
    role: UserRoleEnum
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @field_validator("full_name", "username")
    @classmethod
    def validate_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return value

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    role: UserRoleEnum
    password_hash: str
