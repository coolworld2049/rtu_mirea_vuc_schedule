from fastapi import HTTPException
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser


def get_schedule_parser(
    request: Request,
    course: int,
) -> ScheduleParser:  # pragma: no cover
    schedule_parser = request.app.state.course_workbooks.get(course)
    if not schedule_parser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Schedule for {course} course not found",
        )
    return schedule_parser
