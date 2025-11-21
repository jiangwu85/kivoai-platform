import json
import time
from fastapi import APIRouter
from utils.response import SuccessResponse

app = APIRouter()


@app.get("/", summary="后台任务接口状态")
def app_root(version: str):
    data = {
        "当前时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "test": "后台任务",
        "version": version
    }
    return SuccessResponse(data=data)


@app.get("/list", summary="后台任务列表")
def get_tasks(version: str):
    with open("scripts/tasks.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
    # TODO 改为数据库模式，因为每天更新数据后，需要改变更新事件，数据库更加方便
    return SuccessResponse(data=data)
