from fastapi import FastAPI
import uvicorn
import sentry_sdk

from app.api import api_router
from app.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description='we are the champions',
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router.router)


# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
