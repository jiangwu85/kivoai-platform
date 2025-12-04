import time

from fastapi import APIRouter,Request
from fastapi.encoders import jsonable_encoder
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common

app = APIRouter()


@app.post("/register", summary="register")
async def register(req: Request,reg: Register):
    result = common.register(req.scope["env"], reg)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

@app.post("/login")
async def login(req: Request,lg: Login):
    result = await common.register(req.scope["env"],lg)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

