import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError

from adapter.helper.generate_helper import GenerateHelper
from adapter.transfer.llm_transfer import (
    LlmGenerateRequest,
    LlmGenerateResponse,
)
from application.bus import create_usecase
from application.config import AppConfig, state
from domain.exception.sensitive_exception import SensitiveException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class GenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=10)


class GenerateResponse(BaseModel):
    answer: str


@router.post("/generate", response_model=GenerateResponse)
async def generate_endpoint(
    body: LlmGenerateRequest, config: AppConfig = Depends(state)
):
    try:
        input_data = GenerateHelper.from_request(config, body)

        output_data = await create_usecase(input_data).handle()

        response = GenerateHelper.from_output(output_data)
        return response

    except ValidationError as e:
        logger.exception("Validation error occurred")
        raise HTTPException(status_code=40, detail="Validation Error") from e
    except SensitiveException as e:
        logger.exception("Sensitive exception occurred")
        raise HTTPException(status_code=400, detail="Sensitive Error") from e
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e
