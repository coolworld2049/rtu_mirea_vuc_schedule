import time
from importlib import metadata

# noinspection PyProtectedMember
from cashews import cache
from cashews.contrib.fastapi import (
    CacheDeleteMiddleware,
    CacheEtagMiddleware,
    CacheRequestControlMiddleware,
)
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from schedule_service._logging import configure_logging
from schedule_service.settings import settings
from schedule_service.web.api.v1.router import api_v1_router
from schedule_service.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)


def get_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="RTU MIREA VUC Schedule",
        version=metadata.version("schedule_service"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        expose_headers=["*"],
    )

    app.add_middleware(CacheDeleteMiddleware)
    app.add_middleware(CacheEtagMiddleware)
    app.add_middleware(CacheRequestControlMiddleware)

    register_startup_event(app)
    register_shutdown_event(app)

    cache.setup(settings.redis_url.__str__(), db=0)

    app.include_router(router=api_v1_router)

    @app.get(
        "/health",
        tags=["healthcheck"],
        status_code=status.HTTP_200_OK,
    )
    async def health():
        return {"status": "OK"}

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"{exc}"},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"{exc}"},
        )

    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app
