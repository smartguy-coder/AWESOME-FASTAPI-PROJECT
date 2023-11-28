import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description='we are the champions',
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)
if not os.path.exists('app/templates/qr_images'):
    os.mkdir('app/templates/qr_images')
app.mount('/app/templates/qr_images', StaticFiles(directory='app/templates/qr_images'), name='qr_images')

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
