from fastapi import FastAPI
from app.api import api_router

import sentry_sdk

from settings import project_info
from app.auth import router_auth

app = FastAPI(
    title=project_info.APP_NAME,
    description='we are the champions',
    version=project_info.CURRENT_APP_VERSION,
    debug=project_info.DEBUG,
)

sentry_sdk.init(dsn=project_info.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)
app.include_router(router_auth.router)

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
