from abc import ABC, abstractmethod
from application.config import AppConfig
from typing import Self


class LlmAnswerLogPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    def save(self, key: str) -> None:
        pass
