import time

from fastapi import APIRouter,Request
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common
app = APIRouter()


@app.post("/register", summary="register")
async def app_root(req: Request,register: Register):
    env = req.scope["env"]
    results = await env.DB.prepare('INSERT INTO "main"."user" ("email", "password", "status", "role", "firstName", "lastName", "phone") VALUES(?,?, 9, ?, ?, ?, ?) RETURNING *').bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.phone).run()
    #results = results.results
    result = results.to_py()
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)

@app.post("/login", summary="register")
async def app_root(req: Request,login: Login):
    env = req.scope["env"]
    results = await env.DB.prepare('select * from user where email=?').bind(reg.email).run()
    result = results.to_py()
    # if(result == False):
    #     return ErrorResponse(code=401,data="User password incorrect!")
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)


