from fastapi import APIRouter
from src.llm.llm import LLM
from src.llm.model import Prompt

router = APIRouter(tags=["LLM"])

@router.post("/response")
async def generate_response(prompt: Prompt):
    return await LLM.generate_response(prompt.prompt)