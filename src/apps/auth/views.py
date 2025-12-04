import time

from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common
from core.Auth import authenticate

app = APIRouter()


@app.post("/register", summary="register")
async def register(req: Request,reg: Register):
    result = await common.register(req.scope["env"], reg)
    data = {
        "reg": jsonable_encoder(reg),
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

@app.post("/login")
async def login(req: Request,lg: Login):
    result = await common.login(req.scope["env"],lg)
    data = {
        "lg": jsonable_encoder(lg),
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)


@app.post("/logout")
async def logout(req: Request,token: str = Depends(authenticate)):
    env = req.scope["env"]
    await env.REDIS.delete(token)
    return SuccessResponse(data="OK")