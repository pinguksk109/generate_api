from application.usecase.base import IInput, IOutput, IUsecase
from pydantic import BaseModel, ConfigDict
from application.config import AppConfig
from application.port.llm_port import LlmPort
from application.port.llm_answer_log_port import LlmAnswerLogPort
from application.port.prompt_port import PromptPort
from infrastructure.gemini_repository import GeminiRepository
from infrastructure.dynamodb_prompt_repository import (
    DynamoPromptRepository,
    PromptIds,
)
from infrastructure.s3_llm_answer_log_repository import (
    S3LlmAnswerLogRepository,
)
from domain.llm_answer import Answer
from domain.logic.llm_interaction_helper import LlmInteractionHelper


class GenerateInput(IInput, BaseModel):
    keyword: str
    config: AppConfig


class GenerateOutput(IOutput, BaseModel):
    answer: Answer


class GenerateUsecase(IUsecase):
    class Repository(BaseModel):
        llm: LlmPort
        llm_answer_log: LlmAnswerLogPort
        prompt: PromptPort

        model_config = ConfigDict(arbitrary_types_allowed=True)

    def _reposiory(self):
        llm = GeminiRepository().set_config(self.input_data.config)
        prompt = DynamoPromptRepository().set_config(self.input_data.config)
        llm_answer_log_port = S3LlmAnswerLogRepository().set_config(
            self.input_data.config
        )

        return self.Repository(
            llm=llm, prompt=prompt, llm_answer_log=llm_answer_log_port
        )

    async def handle(self) -> GenerateOutput:
        repository = self._reposiory()

        prompt = await repository.prompt.get_prompt(PromptIds.TRIVIA)

        response = await repository.llm.request(
            prompt, self.input_data.keyword, Answer
        )

        log_key = LlmInteractionHelper.get_log_key(self.input_data.keyword)
        repository.llm_answer_log.save(log_key, response.model_dump_json())

        return GenerateOutput(answer=response)