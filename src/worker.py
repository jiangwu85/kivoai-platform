import jinja2
from workers import WorkerEntrypoint
from js import Response
from fastapi import FastAPI,Request
from application import settings
from application import urls
from core import register_exception
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from utils.tools import import_module
from pyodide.ffi import to_js

environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")
app = FastAPI()
#import_module(settings.MIDDLEWARES, "中间件", app=app)
# 全局异常捕捉处理
register_exception(app)
# 跨域解决
# if settings.CORS_ORIGIN_ENABLE:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.ALLOW_ORIGINS,
#         allow_credentials=settings.ALLOW_CREDENTIALS,
#         allow_methods=settings.ALLOW_METHODS,
#         allow_headers=settings.ALLOW_HEADERS
#     )
# 挂在静态目录
if settings.STATIC_ENABLE:
    app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))
# 引入应用中的路由
for url in urls.urlpatterns:
    app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])

# @app.get("/")
# async def root():
#     message = "This is an example of FastAPI with Jinja2 - go to /hi/<name> to see a template rendered"
#     return {"message": message}
#
#
# @app.get("/hi/{name}")
# async def say_hi(name: str):
#     message = template.render(name=name)
#     return {"message": message}
#
#
@app.get("/env")
async def env(req: Request):
    env = req.scope["env"]
    message = f"Here is an example of getting an environment variable---: {env.MESSAGE}"
    return {"message": message}

@app.get("/redis")
async def redis(req: Request,key: str,val: str):
    env = req.scope["env"]
    await env.REDIS.put(key,val)
    bar = await env.REDIS.get(key)
    return {"val": bar}


@app.get("/db")
async def db(req: Request):
    query = """
            SELECT quote, author
            FROM qtable
            ORDER BY RANDOM() LIMIT 1;
            """
    env = req.scope["env"]
    print("--------1--------")
    results = await env.DB.prepare(query).all()
    return Response.json(results)



@app.get("/db1")
async def db1(req: Request):
    query = """
            SELECT quote, author
            FROM qtable
            ORDER BY RANDOM() LIMIT 1;
            """
    env = req.scope["env"]
    results = await env.DB.prepare(query).all()
    return Response.json(results.results)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi
        return await asgi.fetch(app, request.js_object, self.env)
