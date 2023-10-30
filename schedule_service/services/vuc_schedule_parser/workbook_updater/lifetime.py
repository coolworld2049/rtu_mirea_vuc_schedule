from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from schedule_service.services.vuc_schedule_parser.lifetime import (
    init_vuc_schedule_parser,
)
from schedule_service.services.vuc_schedule_parser.workbook_updater.base import (
    WorkbookUpdater,
)
from schedule_service.settings import workbook_updater_settings


def init_workbook_updater_job(apscheduler: AsyncIOScheduler, app: FastAPI):
    schedule_downloader = WorkbookUpdater()
    apscheduler.add_job(
        schedule_downloader.update_workbooks,
        kwargs={"func": init_vuc_schedule_parser, "app": app},
        trigger="cron",
        id="workbook_updater",
        replace_existing=True,
        **workbook_updater_settings.model_dump(exclude_none=True),
    )


def init_workbook_updater(app: FastAPI) -> None:  # pragma: no cover
    apscheduler = AsyncIOScheduler()
    init_workbook_updater_job(apscheduler, app)
    apscheduler.start()
    app.state.apscheduler = apscheduler


def shutdown_workbook_updater(app: FastAPI) -> None:  # pragma: no cover
    app.state.apscheduler.shutdown(wait=True)
