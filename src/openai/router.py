from fastapi import APIRouter
from src.openai.openai_service import OpenAIService

router = APIRouter(tags=["OpenAI"])

@router.post("/response")
async def get_response(prompt: str):
    return await OpenAIService.get_response(prompt)

