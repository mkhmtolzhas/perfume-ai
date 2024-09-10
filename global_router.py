from fastapi import APIRouter
from src.perfume.router import router as perfume_router
from src.openai.router import router as openai_router

router = APIRouter()

router.include_router(perfume_router, prefix="/perfume")
router.include_router(openai_router, prefix="/ai")