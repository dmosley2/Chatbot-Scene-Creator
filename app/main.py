from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .run_scene import run_scene

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "hello"}

@app.post("/scene")
async def create_scene():
    return await run_scene() 