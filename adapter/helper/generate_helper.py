from adapter.transfer.llm_transfer import (
    LlmGenerateRequest,
    LlmGenerateResponse,
)
from application.config import AppConfig
from application.usecase.generate_usecase import GenerateInput, GenerateOutput


class GenerateHelper:
    @staticmethod
    def from_request(config: AppConfig, req: LlmGenerateRequest):
        return GenerateInput(config=config, keyword=req.keyword)

    @staticmethod
    def from_output(output_data: GenerateOutput):
        return LlmGenerateResponse(answer=output_data.answer.answer)
