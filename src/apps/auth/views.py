import time
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status, Depends, Header
from fastapi.encoders import jsonable_encoder
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common

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
@app.get("/get_headers_with_header")
async def get_headers_with_header(user_agent: str = Header(None), custom_header: str = Header(None)):
    return {
        "User-Agent": user_agent,
        "Custom-Header": custom_header
    }