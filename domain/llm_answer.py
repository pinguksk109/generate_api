from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str
    is_sensitive: bool = Field(
        description="True if the prompt contains sensitive content."
    )
