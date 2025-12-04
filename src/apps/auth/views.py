import time

from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common
from core.Auth import authenticate
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import PyJWTError

app = APIRouter()

SECRET_KEY = "kiavoaivnaoivnaoiwnfvoaiwnfvoainv"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login")
async def login(req: Request,lg: Login):
    result = await common.login(req.scope["env"],lg)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": result["email"]}, expires_delta=access_token_expires
    )
    data = {
        "user": result,
        "accessToken": access_token,
        "tokenType": "bearer",
        "refreshToken": "1",
        "expiresDateTime": access_token_expires,
    }
    return SuccessResponse(data=data)


@app.post("/logout")
async def logout(req: Request,token: str = Depends(authenticate)):
    print("logout token:", token)
    env = req.scope["env"]
    await env.REDIS.delete(token)
    data = {
        "expiresDateTime": time.time()
    }
    return SuccessResponse(data=data)