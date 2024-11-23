import json

from fastapi import APIRouter, WebSocket, Depends
from pydantic import ValidationError

from adapter.transfer.llm_transfer import (
    LlmGenerateRequest,
    LlmGenerateResponse,
)
from adapter.helper.generate_helper import GenerateHelper
from application.config import AppConfig, state
from application.bus import create_usecase

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, config: AppConfig = Depends(state)
):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        message = json.loads(data)

        request = LlmGenerateRequest(keyword=message["keyword"])
        input_data = GenerateHelper.from_request(config, request)
        output_data = await create_usecase(input_data).handle()
        response = GenerateHelper.from_output(output_data)
        await websocket.send_text(response.model_dump_json())
        code, reason = 1000, ""

    except ValidationError as e:
        print(e)
        code, reason = 1003, "Validation Error"
    except Exception as e:
        print(e)
        code, reason = 1011, "Internal Error"
    finally:
        await websocket.close(code, reason)
