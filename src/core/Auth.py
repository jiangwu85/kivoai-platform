
from fastapi import Request, Header, HTTPException

# 鉴权依赖项
async def authenticate(token: str = Header(..., alias="Authorization")):
    print("Authenticating token:", token)
    return token