import json
import logging

from fastapi import APIRouter, WebSocket, Depends
from pydantic import ValidationError

from adapter.transfer.llm_transfer import (
    LlmGenerateRequest,
    LlmGenerateResponse,
)
from adapter.helper.generate_helper import GenerateHelper
from application.config import AppConfig, state
from application.bus import create_usecase
from domain.exception.sensitive_exception import SensitiveException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    except ValidationError:
        logger.exception("Validation error occurred")
        code, reason = 1003, "Validation Error"
    except SensitiveException:
        logger.exception("Sensitive exception occurred")
        code, reason = 4000, "Sensitive Error"
    except Exception:
        logger.exception("Unexpected error occurred")
        code, reason = 1011, "Internal Error"
    finally:
        await websocket.close(code, reason)
