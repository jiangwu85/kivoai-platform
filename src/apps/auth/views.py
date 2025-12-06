import time

from fastapi import APIRouter, Request, HTTPException, Depends, Header
from starlette.status import HTTP_400_BAD_REQUEST
from typing import Any
from fastapi.encoders import jsonable_encoder

from core.moudles import RegisterModel, LoginModel, ProfileModel, LoginSuccessModel
from crud import common
from utils.response import SuccessResponse

app = APIRouter()



@app.post("/register", summary="register")
async def register(req: Request, regModel: RegisterModel):
    result = await common.register(req.scope["env"], regModel)
    return SuccessResponse(loginSuccessResponse(result))

@app.post("/login")
async def login(req: Request, lg: LoginModel):
    result = await common.login(req.scope["env"], lg)
    return SuccessResponse(loginSuccessResponse(result))

async def get_current_user(request: Request,authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Authorization header is required")
    access_token = authorization.replace("Bearer ","")
    return await common.get_user_redis(request.scope["env"], access_token)

@app.get("/me")
async def get_headers_with_header(current_user: Any = Depends(get_current_user)):
    return SuccessResponse(current_user)

@app.put("/profile")
async def profile(request: Request,pfModel: ProfileModel,current_user: Any = Depends(get_current_user)):
    pfModel.id = current_user["id"]
    await common.profile(request.scope["env"], pfModel)
    return SuccessResponse(None)


def loginSuccessResponse(user: Any) -> LoginSuccessModel:
    data = LoginSuccessModel(
        user=user,
        accessToken=str(user["id"]),
        refreshToken=str(user["id"]),
        expiresDateTime=int(time.time())
    )
    return jsonable_encoder(data)