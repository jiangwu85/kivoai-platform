import time
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status, Depends
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

def get_access_token(token: Optional[str] = None, authorization: Optional[str] = None):
    if token:
        return token  # 返回X-Token头部的值
    elif authorization:
        bearer_token = authorization.split(" ")[1]  # 假设是"Bearer <token>"格式
        return bearer_token  # 返回Authorization头部的值
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials"
        )

@app.get("/me")
async def me(accessToken: str = Depends(get_access_token)):
    data = {
        "accessToken": accessToken,
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)