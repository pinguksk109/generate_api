from typing import Optional

from adapter.transfer.trivia_transfer import TriviaGenerateResponse, TriviaGenerateRequest, Item
from application.config import AppConfig
from application.usecase.trivia_quiz_usecase import TriviaQuizInput, TriviaQuizOutput

class TriviaGenerateHelper:
    @staticmethod
    def from_request(config: AppConfig, req: Optional[str]):
        return TriviaQuizInput(config=config, category=req)

    @staticmethod
    def from_output(output_data: TriviaQuizOutput):
        item = Item(quiz=output_data.item.quiz, choices=output_data.item.choices, answer=output_data.item.answer, explanation=output_data.item.explanation)
        return TriviaGenerateResponse(item=item)