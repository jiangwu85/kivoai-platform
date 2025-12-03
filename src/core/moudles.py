
from pydantic import BaseModel
from typing import Optional
class Register(BaseModel):
    role: int
    email: str
    firstName: str
    lastName: str
    phone: Optional[str] = None
    password: str
class Login(BaseModel):
    email: str
    password: str