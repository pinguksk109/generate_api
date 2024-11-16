from typing import Self, Type
from abc import ABC, abstractmethod
from application.config import AppConfig
from pydantic import BaseModel


class LlmPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    async def request(
        self, prompt: str, input_data: str, response_type: Type[BaseModel]
    ):
        pass
