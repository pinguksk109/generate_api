from abc import ABC, abstractmethod


class IInput(ABC):
    pass


class IOutput(ABC):
    pass


class IUsecase(ABC):
    def __init__(self, input_data: IInput):
        self.input_data = input_data

    @abstractmethod
    def handle(self) -> IOutput:
        pass
