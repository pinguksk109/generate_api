from pydantic import BaseModel, Field


class LlmGenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=30)


class LlmGenerateResponse(BaseModel):
    answer: str
