from pydantic import BaseModel, Field, field_validator

class LlmGenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=10)

    @field_validator('keyword')
    def validate_keyword(cls, v):
        if not v or v.strip() == "":
            raise ValueError(f"キーワードが空文字あるいは存在しませんでした+{v}")
        return v