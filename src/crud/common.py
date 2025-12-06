import json

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from typing import Any
from fastapi.encoders import jsonable_encoder

from core.moudles import RegisterModel, LoginModel, ProfileModel, PasswordModel

registerInfo = ['email','password', 'status', 'role']
registerInfoStr = ",".join(registerInfo)
async def register(env: Any,regModel: RegisterModel):
    user = await get_user_by_email(env, regModel.email)
    if user:
        raise HTTPException(HTTP_400_BAD_REQUEST, "email already exists")
    sql = f"INSERT INTO user ({registerInfoStr}) VALUES(?,?,9,?) RETURNING *"
    print(sql)
    results = await env.DB.prepare(sql).bind(regModel.email,regModel.password,regModel.role).run()
    results = results.results[0]
    result = results.to_py()
    await env.REDIS.put(result["id"],json.dumps(jsonable_encoder(result)))
    return result

queryUserInfo = ["id", "email", "status", "role","vip","vipEndTime","firstName","lastName","gender","phone","birthDate","location","bio","createTime","updateTime"]
queryUserInfoStr = ",".join(queryUserInfo)
async def get_user_by_email(env: Any, email: str):
    user = await env.DB.prepare(f"select {queryUserInfoStr} from user where email=?").bind(email).first()
    if user:
        return user.to_py()
    return None

async def get_user_by_id(env: Any, id: int):
    user = await env.DB.prepare(f"select {queryUserInfoStr} from user where id=?").bind(id).first()
    if user:
        return user.to_py()
    return None

async def login(env: Any,lgModel: LoginModel):
    result = await get_user_by_email(env, lgModel.email)
    if not result:
        raise HTTPException(HTTP_401_UNAUTHORIZED, "email or password error!")
    await env.REDIS.put(result["id"],json.dumps(jsonable_encoder(result)))
    return result

async def profile(env: Any,pfModel: ProfileModel):
    await env.DB.prepare(f"update user set firstName=?,lastName=?,gender=?,phone=?,birthDate=?,location=?,bio=? where id=?").bind(pfModel.firstName,pfModel.lastName,pfModel.gender,pfModel.phone,pfModel.birthDate,pfModel.location,pfModel.bio,pfModel.id).run()
    result = await get_user_by_id(env,pfModel.id)
    await env.REDIS.put(result["id"],json.dumps(jsonable_encoder(result)))
    return None

async def password(env: Any,pwModel: PasswordModel):
    await env.DB.prepare(f"update user set password=? where id=?").bind(pwModel.password,pwModel.id).run()
    return None

async def get_user_redis(env: Any,access_token: str):
    user_data = await env.REDIS.get(access_token)
    if not user_data:
        raise HTTPException(HTTP_401_UNAUTHORIZED, "authorization failed")
    user = json.loads(user_data)
    return user






