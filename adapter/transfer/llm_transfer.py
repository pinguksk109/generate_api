from pydantic import BaseModel, Field


class LlmGenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=10)


class LlmGenerateResponse(BaseModel):
    answer: str
