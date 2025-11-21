import time

from fastapi import APIRouter
from utils.response import SuccessResponse

app = APIRouter()


@app.get("/", summary="聊天室接口状态")
def app_root(version: str):
    data = {
        "当前时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "test": "聊天室",
        "version": version
    }
    return SuccessResponse(data=data)

@app.get("/test", summary="test API")
def app_root(version: str):
    data = {
        "当前时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "test": "聊天室",
        "version": version
    }
    return SuccessResponse(data=data)

