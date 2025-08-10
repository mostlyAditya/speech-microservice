
from app.api.v1 import router as api_router
from fastapi import FastAPI
from app.core.config import settings,Settings



def get_application(settings: Settings) -> FastAPI:
    application: FastAPI = FastAPI(
        title=settings.APP_NAME, debug=True, version=settings.VERSION
    )
    application.include_router(api_router)
    return application


app: FastAPI = get_application(settings)