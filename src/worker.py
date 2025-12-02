import jinja2
from workers import WorkerEntrypoint
from fastapi import FastAPI,Request
from application import settings
from application import urls
from core import register_exception
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from utils.tools import import_module

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

@app.get("/db")
async def env(req: Request):
    query = """
        SELECT email, firstName,lastName
        FROM user        
        LIMIT 1;
        """
    results = req.scope["env"].DB.prepare(query).all()
    return {"message": results.results[0]}


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi
        return await asgi.fetch(app, request, self)
