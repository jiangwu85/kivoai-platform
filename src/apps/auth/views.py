import time
from typing import Optional, Any

from fastapi import APIRouter, Request, HTTPException, status, Depends, Header
from fastapi.encoders import jsonable_encoder
from utils.response import SuccessResponse, ErrorResponse
from core.moudles import Register, Login
from crud import common

app = APIRouter()


@app.post("/register", summary="register")
async def register(req: Request, reg: Register):
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
async def login(req: Request, lg: Login):
    result = await common.login(req.scope["env"], lg)
    data = {
        "lg": jsonable_encoder(lg),
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)


async def get_current_user(request: Request):
    headers = request.headers
    access_token = headers.get('authorization')
    print("access_token:"+access_token)
    if not access_token:
        raise ValueError("Missing authentication!")
    return await common.get_user_redis(request.scope["env"], access_token)


@app.get("/me")
async def get_headers_with_header(current_user: Any = Depends(get_current_user)):
    print("current_user:"+current_user)
    return current_user
