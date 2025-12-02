from apps import *


# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": chat, "prefix": "/api/{version}/ws", "tags": ["聊天室"]},
    {"ApiRouter": tasks, "prefix": "/api/{version}/tasks", "tags": ["后台任务"]},
    {"ApiRouter": auth, "prefix": "/api/auth/register", "tags": ["Common API"]},
]
