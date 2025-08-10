from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.models.request_models import TextRequest
from app.services.tts_service import TTSHandler
from app.core.config import settings
from app.utils.file_handlers import cleanup_file
from app.utils.logger import get_logger

logger = get_logger(__name__)

tts_handler = TTSHandler()
router = APIRouter()

@router.post("/speak")
async def synthesize_speech(request: TextRequest, background_tasks: BackgroundTasks):
    logger.info(f"TTS request received")
    try:
        audio_path = tts_handler.synthesize_to_directory(request.text)
        logger.info(f"TTS synthesis done: {audio_path}")
        background_tasks.add_task(cleanup_file, audio_path)
        return FileResponse(
            audio_path,
            media_type=f"audio/{settings.audio_format}",
            filename=f"speech.{settings.audio_format}"
        )
    except Exception as e:
        logger.error(f"TTS synthesis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
