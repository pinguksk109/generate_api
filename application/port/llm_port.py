from abc import ABC, abstractmethod
from typing import Self, Type

from pydantic import BaseModel

from application.config import AppConfig


class LlmPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    async def request(
        self, prompt: str, input_data: str, response_type: Type[BaseModel]
    ):
        pass
