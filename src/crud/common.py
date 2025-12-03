
from fastapi import Request
from core.moudles import Register,Login
def register(req: Request,reg: Register):
    env = req.scope["env"]
    results = env.DB.prepare('INSERT INTO "main"."user" ("email", "password", "status", "role", "firstName", "lastName", "phone") VALUES(?,?, 9, ?, ?, ?, ?) RETURNING *').bind(reg.email,reg.password,reg.role,reg.firstName,reg.lastName,reg.phone).run()
    results = results.results
    results = results.to_py()
    return results

def login(req: Request,reg: Login):
    env = req.scope["env"]
    results = env.DB.prepare('select * from user where email=?').bind(reg.email).run()
    results = results.results
    results = results.to_py()
    # if len(results)==1:
    #     return results[0]
    return results



