from fastapi import APIRouter
from src.perfume.router import router as perfume_router
from src.llm.router import router as llm_router

router = APIRouter()

router.include_router(perfume_router, prefix="/perfume")
router.include_router(llm_router, prefix="/ai")