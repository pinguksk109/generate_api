from application.usecase.base import IInput, IUsecase
from application.usecase.generate_usecase import GenerateInput, GenerateUsecase
from application.usecase.trivia_quiz_usecase import TriviaQuizInput, TriviaQuizUsecase

def create_usecase(input_data: IInput) -> IUsecase:
    input_type = type(input_data)

    if input_type is GenerateInput:
        return GenerateUsecase(input_data)
    elif input_type is TriviaQuizInput:
        return TriviaQuizUsecase(input_data)
    else:
        raise ValueError(f"Invalid input type: {input_type}")
