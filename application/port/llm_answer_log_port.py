from abc import ABC, abstractmethod
from typing import Self

from application.config import AppConfig


class LlmAnswerLogPort(ABC):
    @abstractmethod
    def set_config(self, config: AppConfig) -> Self:
        pass

    @abstractmethod
    def save(self, key: str, body: str) -> None:
        pass
