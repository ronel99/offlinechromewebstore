from fastapi import APIRouter

router = APIRouter()

from .extensions import router as extensions_router

router.include_router(extensions_router)