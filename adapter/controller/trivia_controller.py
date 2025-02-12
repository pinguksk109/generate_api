import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from adapter.helper.trivia_generate_helper import TriviaGenerateHelper
from adapter.transfer.trivia_transfer import TriviaGenerateRequest, TriviaGenerateResponse
from application.bus import create_usecase
from application.config import AppConfig, state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/trivia_quiz", response_model=TriviaGenerateResponse)
async def trivia_quiz_generate(body: Optional[TriviaGenerateRequest] = None, config: AppConfig = Depends(state)):
    try:
        category = body.category if body is not None else None

        input_data = TriviaGenerateHelper.from_request(config, category)

        output_data = await create_usecase(input_data).handle()

        response = TriviaGenerateHelper.from_output(output_data)
        return response
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500)