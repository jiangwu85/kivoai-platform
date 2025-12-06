import time

from fastapi import APIRouter, Request, HTTPException, Depends, Header
from starlette.status import HTTP_400_BAD_REQUEST
from typing import Any

from core.moudles import Register, Login, Profile
from crud import common
from utils.response import SuccessResponse

app = APIRouter()


@app.post("/register", summary="register")
async def register(req: Request, reg: Register):
    result = await common.register(req.scope["env"], reg)
    data = {
        "user": result,
        "accessToken": result["id"],
        "refreshToken": result["id"],
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

@app.post("/login")
async def login(req: Request, lg: Login):
    result = await common.login(req.scope["env"], lg)
    data = {
        "user": result,
        "accessToken": result["id"],
        "refreshToken": result["id"],
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

async def get_current_user(request: Request,authorization: str = Header(None)):
    print("access_token:"+authorization)
    if not authorization:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Authorization header is required")
    access_token = authorization.replace("Bearer ","")
    return await common.get_user_redis(request.scope["env"], access_token)

@app.get("/me")
async def get_headers_with_header(current_user: Any = Depends(get_current_user)):
    return SuccessResponse(data=current_user)

@app.get("/profile")
async def profile(request: Request,pf: Profile,current_user: Any = Depends(get_current_user)):
    pf.id = current_user.id
    await common.profile(env=request.scope["env"], pf=pf)
    return SuccessResponse(data=True)
