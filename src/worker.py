import jinja2
from fastapi import FastAPI, Request,APIRouter
from workers import WorkerEntrypoint

environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")

app = FastAPI()
router_v1 = APIRouter()
router_v2 = APIRouter()

@router_v1.get("/items/")
def get_items():
    return {"message": "This is from v1"}


@router_v2.get("/")
async def root():
    message = "This is an example of FastAPI with Jinja2 - go to /hi/<name> to see a template rendered"
    return {"message": message}


@router_v2.get("/hi/{name}")
async def say_hi(name: str):
    message = template.render(name=name)
    return {"message": message}


@router_v2.get("/env")
async def env(req: Request):
    env = req.scope["env"]
    message = f"Here is an example of getting an environment variable---: {env.MESSAGE}"
    return {"message": message}


app.include_router(router_v1, prefix="/v1")
app.include_router(router_v2, prefix="/v2")

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi
        return await asgi.fetch(app, request.js_object, self.env)
