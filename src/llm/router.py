from fastapi import APIRouter
from src.llm.llm import LLM

router = APIRouter(tags=["LLM"])

@router.post("/response")
async def generate_response(prompt: str):
    return await LLM.generate_response(prompt)