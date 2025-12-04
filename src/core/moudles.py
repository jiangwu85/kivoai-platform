
from pydantic import BaseModel,Field
from typing import Optional
class Register(BaseModel):
    role: int
    email: str
    password: str
    firstName: str
    lastName: str
    gender: Optional[int] = Field(description="gender",default=1,ge=0,le=1)
    phone: Optional[str] = Field(description="phone",default="")
    birthDate: Optional[str] = Field(description="birth date",default="")
    location: Optional[str] = Field(description="location",default="")
    bio: Optional[str] = Field(description="bio",default="")
class Login(BaseModel):
    email: str
    password: str