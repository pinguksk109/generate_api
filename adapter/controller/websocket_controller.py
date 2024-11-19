import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from adapter.transfer.llm_transfer import (
    LlmGenerateRequest,
    LlmGenerateResponse,
)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        message = json.loads(data)

        request = LlmGenerateRequest(keyword=message["keyword"])
        response = LlmGenerateResponse(answer=request.keyword)

        await websocket.send_text(response.answer)
        code, reason = 1000, ""

    except ValidationError:
        code, reason = 1003, "Validation Error"
    finally:
        await websocket.close(code, reason)
