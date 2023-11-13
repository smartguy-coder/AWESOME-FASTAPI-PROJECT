from fastapi import FastAPI
from app.api import api_router
import sentry_sdk

app = FastAPI(
    title='First our app',
    description='we are champions',
    version='0.1.0',
    debug=True
)

sentry_sdk.init(
    dsn="https://9b3663d08026ab47cd90ceaa5478837d@o4505760997834752.ingest.sentry.io/4506214623543296",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app.include_router(api_router.router)
