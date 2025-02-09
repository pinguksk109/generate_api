from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, Field

from application.config import AppConfig
from application.port.llm_port import  LlmPort
from application.port.llm_answer_log_port import LlmAnswerLogPort
from application.usecase.base import IInput, IOutput, IUsecase
from infrastructure.gemini_repository import GeminiRepository
from infrastructure.s3_llm_answer_log_repository import S3LlmAnswerLogRepository
from domain.exception.sensitive_exception import SensitiveException
from langchain.prompts import PromptTemplate

class Item(BaseModel):
    quiz: str
    choices: List[str]
    answer: int
    explanation: str

class Answer(BaseModel):
    item: List[Item]
    is_sensitive: bool = Field(
        description="True if the prompt contains sensitive content."
    )

class TriviaQuizInput(IInput, BaseModel):
    config: AppConfig
    category: Optional[str] = None

class TriviaQuizOutput(IOutput, BaseModel):
    item: List[Item]

class TriviaQuizUsecase(IUsecase):
    class Repository(BaseModel):
        llm: LlmPort
        llm_log: LlmAnswerLogPort
        model_config = ConfigDict(arbitrary_types_allowed=True)

    def _repository(self):
        llm = GeminiRepository().set_config(self.input_data.config)
        llm_log_port = S3LlmAnswerLogRepository().set_config(self.input_data.config)

        return self.Repository(llm=llm, llm_log=llm_log_port)

    async def handle(self) -> TriviaQuizOutput:
        repository = self._repository()

        if self.input_data.category is not None:
            with open("./prompt/trivia_quiz_with_category_prompt.txt", "r", encoding="utf-8") as file:
                raw_prompt = file.read()
                prompt_template = PromptTemplate(
                    input_variables=["keyword"],
                    template=raw_prompt,
                )
                prompt = prompt_template.format(keyword=self.input_data.category)
        else:
            with open("./prompt/trivia_quiz_prompt.txt", "r", encoding="utf-8") as file:
                raw_prompt = file.read()
                prompt_template = PromptTemplate(
                    input_variables=["keyword"],
                    template=raw_prompt,
                )
                prompt = prompt_template.format()

        print(prompt)

        response = await repository.llm.request(prompt, Answer)
        print(response)
        if response.is_sensitive:
            raise SensitiveException()

        return TriviaQuizOutput(answer=response.item)
