import os

VERSION = "2.0.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
挂载静态目录，并添加路由访问，此路由不会在接口文档中显示
STATIC_ENABLE：是否启用静态目录
STATIC_URL：路由访问
STATIC_ROOT：静态文件目录相对路径
官方文档：https://fastapi.tiangolo.com/tutorial/static-files/
"""
STATIC_ENABLE = False
STATIC_URL = "/static"
STATIC_ROOT = "./static"
STATIC_DIR = os.path.join(BASE_DIR, "static")


"""
跨域解决
详细解释：https://cloud.tencent.com/developer/article/1886114
官方文档：https://fastapi.tiangolo.com/tutorial/cors/
"""
# 是否启用跨域
CORS_ORIGIN_ENABLE = True
# 只允许访问的域名列表，* 代表所有
ALLOW_ORIGINS = ["*"]
# 是否支持携带 cookie
ALLOW_CREDENTIALS = True
# 设置允许跨域的http方法，比如 get、post、put等。
ALLOW_METHODS = ["*"]
# 允许携带的headers，可以用来鉴别来源等作用。
ALLOW_HEADERS = ["*"]

# 数据库配置项
SQLALCHEMY_DATABASE_ENABLE = False
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/customer"

# Redis 数据库配置项
REDIS_DB_ENABLE = False
REDIS_DB_URL = "redis://:123456@127.0.0.1:6379/0"

"""
全局事件配置
"""
EVENTS = [
    "core.event.connect_redis" if REDIS_DB_ENABLE else None,
]

"""
中间件配置
"""
MIDDLEWARES = [
    "core.middleware.register_middleware"
]
