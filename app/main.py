from fastapi import FastAPI
from app.api import api_router
import sentry_sdk
from settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description='we are champions',
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)
