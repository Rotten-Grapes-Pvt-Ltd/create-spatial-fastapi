from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import items # add router

from database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(items.router, prefix="/items", tags=["items"]) # include router

@app.get("/")
def read_root():
    return {"Hello": "World"}
