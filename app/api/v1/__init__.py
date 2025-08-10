from fastapi import APIRouter

from app.api.v1 import tts

router = APIRouter()

router.include_router(tts.router, tags=["tts"], prefix="/v1")