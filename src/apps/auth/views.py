import time

from fastapi import APIRouter,Request
from utils.response import SuccessResponse,ErrorResponse
from core.moudles import Register,Login
from crud import common
import orjson

app = APIRouter()


@app.post("/register", summary="register")
async def register(req: Request,reg: Register):
    env = req.scope["env"]
    results = await env.DB.prepare('INSERT INTO "user" ("email", "password", "status", "role", "firstName", "lastName", "phone") VALUES(?,?, 9, ?, ?, ?, ?) RETURNING *').bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.phone).run()
    #results = results.results
    result = results.to_py()
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)


@app.post("/register1", summary="register")
async def register1(req: Request,reg: Register):
    result = common.register(req,reg)
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return SuccessResponse(data=data)

@app.get("/db")
async def db(req: Request):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user").run()
    results = results.results
    results = results.to_py()
    # Return a JSON response
    return results
@app.get("/db0")
async def db(req: Request):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user").run()
    results = results.results
    results = results.to_py()
    # Return a JSON response
    return SuccessResponse(data=results)
@app.get("/db1")
async def db1(req: Request):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user").run()
    results = results.results
    results = results.to_py()
    # Return a JSON response
    return {"code": 200,"message": "success","data": results}
@app.post("/login")
async def login(req: Request,lg: Login):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user where email=?").bind(lg.email).run()
    results = results.results
    result = results.to_py()
    data = {
        "user": result,
        "accessToken": "1",
        "refreshToken": "1",
        "expiresDateTime": time.time_ns(),
    }
    return {"code": 200,"message": "success","data": data}