import time

from fastapi import APIRouter,Request
from utils.response import SuccessResponse
from pydantic import BaseModel
from typing import Optional
app = APIRouter()

class Register(BaseModel):
    role: int
    email: str
    firstName: str
    lastName: str
    phone: Optional[str] = None
    password: str
@app.post("/register", summary="register")
async def app_root(req: Request,register: Register):
    data = {
        "当前时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "test": "聊天室",
        "register": register.dict()
    }

    return SuccessResponse(data=data)

