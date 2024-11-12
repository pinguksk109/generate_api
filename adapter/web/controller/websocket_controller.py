import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from typing import List
import asyncio

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)

                if "keyword" in message:
                    keyword = message["keyword"]

                    await asyncio.sleep(5)
                    response = f"Received keyword: {keyword}"
                    await websocket.send_text(response)
                else:
                    response = "keyword not found"
                break

            except ValueError as e:
                error_message = f"Validation error: {e}"
                await websocket.send_text(error_message)

            except Exception:
                await websocket.send_text(response)
                break

    except WebSocketDisconnect:
        pass

    finally:
        await websocket.close()