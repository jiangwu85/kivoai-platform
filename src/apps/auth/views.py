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
    result = common.register(req.scope["env"],lg)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)



@app.post("/register1", summary="register")
async def register1(req: Request,reg: Register):
    env = req.scope["env"]
    results = await env.DB.prepare('INSERT INTO "user" ("email", "password", "status", "role", "firstName", "lastName", "phone") VALUES(?,?, 9, ?, ?, ?, ?) RETURNING *').bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.phone).run()
    results = results.results[0]
    result = results.to_py()
    result = jsonable_encoder(result)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)

@app.post("/login1")
async def login1(req: Request,lg: Login):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user where email=?").bind(lg.email).run()
    result = results.results[0]
    result = jsonable_encoder(result.to_py())
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time(),
    }
    return SuccessResponse(data=data)
