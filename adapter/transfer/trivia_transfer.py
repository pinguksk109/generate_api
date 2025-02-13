from pydantic import BaseModel, Field
from typing import List, Optional

class Item(BaseModel):
    quiz: str = Field
    choices: List[str] = Field
    answer: int = Field
    explanation: str = Field

    # class Config:
    #     populate_by_name = True

class TriviaGenerateRequest(BaseModel):
    category: Optional[str]

class TriviaGenerateResponse(BaseModel):
    item: Item