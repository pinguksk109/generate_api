from application.usecase.base import IInput, IUsecase
from application.usecase.generate_usecase import GenerateUsecase, GenerateInput


def create_usecase(input_data: IInput) -> IUsecase:
    input_type = type(input_data)

    if input_type is GenerateInput:
        return GenerateUsecase(input_data)
    else:
        raise ValueError(f"Invalid input type: {input_type}")
