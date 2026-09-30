from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .run_scene import run_scene

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/portraits", StaticFiles(directory="personas/images"), name="portraits")

@app.get("/")
async def root():
    return {"message": "hello"}

@app.post("/scene")
async def create_scene():
    return await run_scene()

@app.websocket("/ws/scene")
async def scene_websocket(websocket: WebSocket):
    await websocket.accept()
    await run_scene(websocket.send_json)
    await websocket.close()
 