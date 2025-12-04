
from fastapi.encoders import jsonable_encoder
from core.moudles import Register,Login
from typing import Any
async def register(env: Any,reg: Register):
    results = await env.DB.prepare("INSERT INTO user (email,password,status,role,firstName,lastName,gender, phone,birthDate,location,bio) VALUES(?,?,9,?,?,?, ?,?,?,?,?) RETURNING *").bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.gender,reg.phone,reg.birthDate,reg.location,reg.bio).run()
    results = results.results[0]
    result = results.to_py()
    return jsonable_encoder(result)

async def login(env: Any,lg: Login):
    results = await env.DB.prepare("select email,status,role,firstName,lastName,gender,phone,birthDate,location,bio from user where email=?").bind(lg.email).run()
    result = results.results[0]
    return jsonable_encoder(result.to_py())




