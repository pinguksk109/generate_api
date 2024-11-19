from abc import ABC, abstractmethod
from enum import Enum
from typing import Self, Type

from application.config import AppConfig


class PromptPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    async def get_prompt(self, prompt_id: Type[Enum]) -> str:
        pass
