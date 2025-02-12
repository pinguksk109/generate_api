from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    quiz: str
    choices: List[str]
    answer: int
    explanation: str

class TriviaGenerateRequest(BaseModel):
    category: Optional[str]

class TriviaGenerateResponse(BaseModel):
    item: Item