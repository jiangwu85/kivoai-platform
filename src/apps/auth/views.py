import time

from fastapi import APIRouter,Request
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common
app = APIRouter()


@app.post("/register", summary="register")
async def app_root(req: Request,register: Register):
    result = await common.register(req,register)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)

@app.post("/login", summary="register")
async def app_root(req: Request,login: Login):
    result = await common.login(req,login)
    # if(result == False):
    #     return ErrorResponse(code=401,data="User password incorrect!")
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)


