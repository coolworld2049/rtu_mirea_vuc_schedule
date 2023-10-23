from starlette.requests import Request

from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser


def get_workbook_parsers(
    request: Request,
) -> dict[int, ScheduleParser]:  # pragma: no cover
    return request.app.state.workbook_parsers
