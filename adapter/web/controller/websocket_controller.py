import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)

                if "keyword" in message:
                    keyword = message["keyword"]

                    await asyncio.sleep(5)
                    response = f"Received keyword: {keyword}"
                    await manager.send_message(response, websocket)
                else:
                    response = "keyword not found"
                await websocket.close()
                break

            except Exception:
                await manager.send_message("Invalid Json format", websocket)
                await websocket.close()
                break

    except WebSocketDisconnect:
        pass

    finally:
        manager.disconnect(websocket)