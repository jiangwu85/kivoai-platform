
from fastapi import Request, Header, HTTPException

# 鉴权依赖项
async def authenticate(req: Request, token: str = Header(..., alias="Authorization")):
    print("Authenticating token:", token)
    env = req.scope["env"]
    val = await env.REDIS.get(token)
    if val is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return token