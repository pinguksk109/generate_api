from application.usecase.base import IInput, IOutput, IUseCase
from pydantic import BaseModel
from application.config import AppConfig


class Answer:
    answer: str


class GenereteInput(IInput, BaseModel):
    keyword: str


class GptGenerateOutput(IOutput, BaseModel):
    answer: Answer


class GenerateUsecase(IUsecase):