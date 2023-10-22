import tenacity
from fastapi import FastAPI
from loguru import logger

from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser
from schedule_service.settings import settings


@tenacity.retry(
    retry=tenacity.retry_if_result(lambda result: not result),
    wait=tenacity.wait_fixed(6),
    stop=tenacity.stop_after_delay(100),
    reraise=True,
)
def get_course_workbooks(courses: list[int] | None = None):
    course_workbooks = {}
    try:
        if courses:
            course_workbook_objects = list(
                filter(lambda c: c.course in courses, settings.course_workbooks)
            )
        else:
            course_workbook_objects = settings.course_workbooks
        for cw in course_workbook_objects:
            schedule_parser = ScheduleParser(
                workbook_path=cw.workbook_path,
                workbook_settings=cw.workbook_settings,
                workbook_settings_path=cw.workbook_settings_path,
            )
            course_workbooks.update({cw.course: schedule_parser})
    except Exception as e:
        logger.error(e)
    return course_workbooks


def init_schedule_parser(app: FastAPI) -> None:  # pragma: no cover
    # schedule_downloader = ScheduleDownloader()
    # schedule_downloader.update_workbooks()
    app.state.course_workbooks = get_course_workbooks()


def shutdown_schedule_parser(app: FastAPI) -> None:  # pragma: no cover
    for k, v in app.state.course_workbooks.items():
        v.close()
