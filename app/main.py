from fastapi import FastAPI
from app.api import api_router

import sentry_sdk

from app.settings import settings
from app.auth import router_auth

app = FastAPI(
    title=settings.APP_NAME,
    description='we are the champions',
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)
app.include_router(router_auth.router)

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
