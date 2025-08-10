from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "TTS Microservice"
    VERSION: str = "1.0.0"
    max_text_length: int = 1000
    audio_format: str = "mp3"
    
    TTS_FOLDER: str = "app/audio_files"
    
    class Config:
        env_file = ".env"

settings = Settings()