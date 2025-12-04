
from pydantic import BaseModel
from typing import Optional
class Register(BaseModel):
    role: int
    email: str
    password: str
    firstName: str
    lastName: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    birthDate: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
class Login(BaseModel):
    email: str
    password: str