from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from schedule_service.services.vuc_schedule_parser.lifetime import get_course_workbooks
from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser
from schedule_service.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def fastapi_app() -> FastAPI:
    application = get_app()
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def schedule_parser_instance(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> ScheduleParser:
    course = 4
    course_workbooks = get_course_workbooks([course])
    schedule_parser = course_workbooks.get(course)
    return schedule_parser
