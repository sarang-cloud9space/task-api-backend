
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from routers.auth_routes import router as auth_router
from routers.task_routes import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run startup and shutdown logic here.
    yield
    await engine.dispose()


app = FastAPI(
    title="Tasks API",
    description="Tasks API with PostgreSQL and JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the browser frontend (a different origin) to call this API.
# Set CORS_ORIGINS on the host, e.g. https://my-app.vercel.app
origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def root():
    return {"message": "Tasks API is running"}
