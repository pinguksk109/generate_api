from typing import Self, Type
from abc import ABC, abstractmethod
from application.config import AppConfig
from enum import Enum


class PromptPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    async def get_prompt(self, prompt_id: Type[Enum]) -> str:
        pass
