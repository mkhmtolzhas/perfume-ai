from fastapi import APIRouter, HTTPException
from src.llm.llm import LLM
from src.llm.model import Prompt

router = APIRouter(tags=["LLM"])

@router.post("/response")
async def generate_response(prompt: Prompt):
    try:
        return await LLM.generate_response(prompt.prompt)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))