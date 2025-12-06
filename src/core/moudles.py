import time

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from core.validator import vali_email



class LoginModel(BaseModel):
    email: str = Field(min_length=5,  default="273617974@qq.com")
    password: str = Field(min_length=6, default="123456")
    @field_validator('email')
    def check_email(cls, v):
        return vali_email(v)

class RegisterModel(LoginModel):
    role: int

class ProfileModel(BaseModel):
    id: Optional[int] = Field(default=0)
    firstName: str = Field(min_length=2, default="Jiang")
    lastName: str = Field(min_length=2, default="Wu")
    gender: Optional[int] = Field(default=1)
    phone: Optional[str] = Field(default="")
    birthDate: Optional[str] = Field(default="")
    location: Optional[str] = Field(default="")
    bio: Optional[str] = Field(default="")

class LoginSuccessModel(BaseModel):
    user: Any
    accessToken: str
    refreshToken: str
    expiresDateTime: int


