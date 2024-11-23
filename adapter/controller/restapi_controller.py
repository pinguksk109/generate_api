from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError

router = APIRouter()


class GenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=10)


class GenerateResponse(BaseModel):
    answer: str


@router.get("/generate", response_model=GenerateResponse)
async def generate_endpoint(request: GenerateRequest):
    response = GenerateResponse(answer=f"{request.keyword}")
    return response
