from starlette.requests import Request

from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser


def get_workbook_parsers(
    request: Request,
) -> ScheduleParser:  # pragma: no cover
    course_dir = f"{request.query_params.get('course')}-course"
    return request.app.state.workbook_parsers.get(course_dir)
