from fastapi import FastAPI
from app.api import api_router
from fastapi.staticfiles import StaticFiles

import sentry_sdk

from app.settings import Settings

app = FastAPI(
    title=Settings.APP_NAME,
    description='we are the champions',
    version=Settings.CURRENT_APP_VERSION,
    debug=Settings.DEBUG,
)

app.mount('/app/templates/qr_images', StaticFiles(directory='app/templates/qr_images'), name='qr_images')

sentry_sdk.init(dsn=Settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
