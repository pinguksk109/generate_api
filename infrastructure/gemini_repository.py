from typing import Self, Type

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from application.config import AppConfig
from application.port.llm_port import LlmPort


class GeminiRepository(LlmPort):
    def __init__(self):
        self._config = None
        self._model = None

    def set_config(self, config: AppConfig) -> Self:
        self._config = config
        self._model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", api_key=config.env.gemini_api_key
        )
        return self

    async def request(self, prompt: str, response_type: Type[BaseModel]):

        llm = self._model.with_structured_output(response_type)
        response = llm.invoke(prompt)

        return response
