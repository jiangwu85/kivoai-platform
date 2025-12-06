import json

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from core.moudles import Register, Login, Profile
from typing import Any
from starlette.status import HTTP_400_BAD_REQUEST

registerInfo = ['email','password', 'status', 'role']
registerInfoStr = ",".join(registerInfo)
async def register(env: Any,reg: Register):
    user = await get_user_by_email(env, reg.email)
    if user:
        raise HTTPException(status_code=400, detail="email already exists")
    sql = f"INSERT INTO user ({registerInfoStr}) VALUES(?,?,9,?) RETURNING *"
    print(sql)
    results = await env.DB.prepare(sql).bind(reg.email,reg.password,reg.role).run()
    user = results.results[0]
    #await env.REDIS.put(user["id"],json.dumps(jsonable_encoder(user.to_py())))
    return user

queryUserInfo = ["id", "email", "status", "role","vip","vipEndTime","firstName","lastName","gender","phone","birthDate","location","bio","createTime","updateTime"]
queryUserInfoStr = ",".join(queryUserInfo)
async def get_user_by_email(env: Any, email: str):
    user = await env.DB.prepare(f"select {queryUserInfoStr} from user where email=?").bind(email).first()
    if user:
        return user
    return None

async def get_user_by_id(env: Any, id: int):
    user = await env.DB.prepare(f"select {queryUserInfoStr} from user where id=?").bind(id).first()
    if user:
        return user
    return None

async def login(env: Any,lg: Login):
    user = await get_user_by_email(env, lg.email)
    if not user:
        raise HTTPException(status_code=400, detail="email or password error!")
    #await env.REDIS.put(user["id"],json.dumps(jsonable_encoder(user.to_py())))
    return user

async def profile(env: Any,pf: Profile):
    await env.DB.prepare(f"update user set firstName=?,lastName=?,gender=?,phone=?,birthDate=?,location=?,bio=? where id=?").bind(pf.firstName,pf.lastName,pf.gender,pf.phone,pf.birthDate,pf.location,pf.bio,pf.id).run()
    user = await get_user_by_id(env,pf.id)
    #await env.REDIS.put(user["id"],json.dumps(jsonable_encoder(user.to_py())))
    return None

async def get_user_redis(env: Any,access_token: str):
    user_data = await env.REDIS.get(access_token)
    if not user_data:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="authorization failed")
    user = json.loads(user_data).to_py()
    return user






