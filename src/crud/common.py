import json

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core.moudles import Register,Login
from typing import Any
from starlette.status import HTTP_400_BAD_REQUEST

async def register(env: Any,reg: Register):
    results = await (env.DB.prepare("INSERT INTO user (email,password,status,role,firstName,lastName,gender, phone,birthDate,location,bio) VALUES(?,?,9,?,?,?, ?,?,?,?,?) RETURNING *").bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.gender,reg.phone,reg.birthDate,reg.location,reg.bio).run())
    results = results.results[0]
    result = results.to_py()
    result = jsonable_encoder(result)
    return result

async def login(env: Any,lg: Login):
    results = await env.DB.prepare("select id,email,status,role,firstName,lastName,gender,phone,birthDate,location,bio from user where email=?").bind(lg.email).run()
    result = results.results[0]
    result = jsonable_encoder(result.to_py())
    return result

async def get_user_redis(env: Any,access_token: str):
    user_data = await env.REDIS.get(access_token)
    if not user_data:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="authorization failed")
    user = json.loads(user_data)
    return user






