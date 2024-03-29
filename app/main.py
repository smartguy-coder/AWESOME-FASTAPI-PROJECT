import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api import api_router_auth, api_router_user
from app.settings import settings
from app.web import web_auth_router, web_login_router

app = FastAPI(
    title=settings.APP_NAME,
    description="we are the champions",
    version=settings.CURRENT_APP_VERSION,
    debug=settings.DEBUG,
)
app.add_middleware(GZipMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1'])

sentry_sdk.init(dsn=settings.SENTRY_SDK_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app.include_router(api_router_user.router)
app.include_router(api_router_auth.guest_router)
app.include_router(api_router_auth.auth_protected_router)

app.include_router(web_auth_router.router)
app.include_router(web_login_router.router)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

# TODO: temporary disable to check regular web endpoints. In future useful for REACT
# app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')

# for using in templates url_for(<function_name>) instead of hardcoded path
# https://stackoverflow.com/questions/63682956/fastapi-retrieve-url-from-view-name-route-name
# based on main app instance
# print(app.url_path_for('get_latest_stories'))

if __name__ == "__main__":  # pragma: no cover
    # useful for debug mode
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)  # pragma: no cover
