
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from core.validator import vali_email

class Login(BaseModel):
    email: str = Field(min_length=5,  default="273617974@qq.com")
    password: str = Field(min_length=6, default="123456")

    @field_validator('email')
    def check_email(cls, v):
        return vali_email(v)

class Register(Login):
    role: int

class Profile(BaseModel):
    id: int
    firstName: str = Field(min_length=2, default="Jiang")
    lastName: str = Field(min_length=2, default="Wu")
    gender: Optional[int] = Field(default=1)
    phone: Optional[str] = Field(default="")
    birthDate: Optional[str] = Field(default="")
    location: Optional[str] = Field(default="")
    bio: Optional[str] = Field(default="")