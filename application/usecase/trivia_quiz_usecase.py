from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from application.config import AppConfig
from application.port.llm_port import  LlmPort
from application.usecase.base import IInput, IOutput, IUsecase
from infrastructure.gemini_repository import GeminiRepository
from langchain.prompts import PromptTemplate

class Item(BaseModel):
    quiz: str
    choices: List[str]
    answer: int
    explanation: str

class TriviaQuizInput(IInput, BaseModel):
    config: AppConfig
    category: Optional[str] = None

class TriviaQuizOutput(IOutput, BaseModel):
    item: Item

class TriviaQuizUsecase(IUsecase):
    class Repository(BaseModel):
        llm: LlmPort
        model_config = ConfigDict(arbitrary_types_allowed=True)

    def _repository(self):
        llm = GeminiRepository().set_config(self.input_data.config)

        return self.Repository(llm=llm)

    async def handle(self) -> TriviaQuizOutput:
        repository = self._repository()

        if self.input_data.category is not None:
            with open("./prompt/trivia_quit_with_category_prompt.txt", "r", encoding="utf-8") as file:
                raw_prompt = file.read()
                prompt_template = PromptTemplate(
                    input_variables=["category"],
                    template=raw_prompt,
                )
                prompt = prompt_template.format(category=self.input_data.category)
        else:
            with open("./prompt/trivia_quiz_prompt.txt", "r", encoding="utf-8") as file:
                raw_prompt = file.read()
                prompt_template = PromptTemplate(
                    template=raw_prompt,
                )
                prompt = prompt_template.format()

        response = await repository.llm.request(prompt, Item)
        return TriviaQuizOutput(item=response)
