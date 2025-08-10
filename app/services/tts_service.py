from gtts import gTTS
import tempfile
from pathlib import Path
from typing import Optional, Union
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class TTSHandler:
    def __init__(self):
        logger.info("Google TTS Handler initialized")
        self.supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']

    def synthesize_gtts(self, text: str, output_path: Optional[Union[str, Path]] = settings.TTS_FOLDER, language: str = 'en') -> Path:
        try:
            if language not in self.supported_languages:
                language = 'en'
            if not output_path:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    output_path = Path(tmp_file.name)
            else:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                if not output_path.suffix or output_path.suffix.lower() != '.mp3':
                    output_path = output_path.with_suffix(".mp3")
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(output_path))
            if not output_path.exists() or output_path.stat().st_size == 0:
                raise Exception("Google TTS synthesis failed - output file not created or empty")
            return output_path
        except Exception as e:
            logger.error(f"Google TTS synthesis failed: {e}")
            raise

    def synthesize_to_directory(self, text: str, directory: Optional[Union[str, Path]] = None, filename: Optional[str] = None, language: str = 'en') -> Path:
        if not directory:
            directory = getattr(settings, 'TTS_FOLDER', 'output')
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_output_{timestamp}.mp3"
        elif not filename.endswith('.mp3'):
            filename = f"{filename}.mp3"
        output_path = directory / filename
        return self.synthesize_gtts(text, output_path, language)

    def get_supported_languages(self):
        """Return list of supported language codes"""
        return self.supported_languages