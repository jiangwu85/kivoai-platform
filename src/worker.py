from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
from pydantic import BaseModel
import asgi

SDB = None  # Placeholder for database connection if needed
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        SDB = self.env.DB
        return await asgi.fetch(app, request, self.env)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/env")
async def root(req: Request):
    env = req.scope["env"]
    query = """
        SELECT quote, author
        FROM qtable
        ORDER BY RANDOM()
        LIMIT 1;
        """
    results = SDB.prepare(query).all()
    data = results.results[0]
    return {"message": "Here is an example of getting an environment variable: " + env.MESSAGE,"data": data}

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"qq": q})
    return result

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}