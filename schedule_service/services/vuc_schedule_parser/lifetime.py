from fastapi import FastAPI
from loguru import logger

from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser
from schedule_service.settings import settings


def get_workbook_parsers(course_dirs: list[str] | None = None):
    workbook_parsers = {}
    if course_dirs:
        workbook_files = list(
            filter(lambda c: c.course_dir in course_dirs, settings.workbook_files),
        )
    else:
        workbook_files = settings.workbook_files
    for wf in workbook_files:
        schedule_parser = ScheduleParser(
            workbook_path=wf.workbook_path,
            workbook_settings=wf.workbook_settings,
            workbook_settings_path=wf.workbook_settings_path,
        )
        workbook_parsers.update({wf.course_dir: schedule_parser})
    logger.info("All workbook parsers are loaded")
    return workbook_parsers


def init_vuc_schedule_parser(app: FastAPI) -> None:  # pragma: no cover
    app.state.workbook_parsers = get_workbook_parsers()


def shutdown_vuc_schedule_parser(app: FastAPI) -> None:  # pragma: no cover
    for k, v in app.state.workbook_parsers.items():
        v.close()
