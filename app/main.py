import sentry_sdk
import uvicorn
from fastapi import FastAPI

from app.api import api_router_auth, api_router_stories, api_router_user
from app.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="we are the champions",
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router_stories.router)
app.include_router(api_router_user.router)
app.include_router(api_router_auth.guest_router)
app.include_router(api_router_auth.auth_protected_router)

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')

if __name__ == "__main__":  # pragma: no cover
    # useful for debug mode
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)  # pragma: no cover
