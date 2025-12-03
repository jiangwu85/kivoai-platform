
from fastapi import Request
from core.moudles import Register,Login
async def register(req: Request,reg: Register):
    env = req.scope["env"]
    results = await env.DB.prepare("INSERT INTO user (email, password, status, role, firstName, lastName, phone) VALUES(?,?, 9, ?, ?, ?, ?) RETURNING *").bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.phone).run()
    results = results.results
    results = results.to_py()
    return results

async def login(req: Request,lg: Login):
    env = req.scope["env"]
    results = await env.DB.prepare("select * from user where email=?").bind(lg.email).run()
    #results = results.results
    results = results.to_py()
    # if len(results)==1:
    #     return results[0]
    return results



