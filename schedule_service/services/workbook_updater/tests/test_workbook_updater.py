from schedule_service.services.vuc_schedule_parser.lifetime import get_course_workbooks
from schedule_service.services.workbook_updater.__main__ import ScheduleWorkbookUpdater


def test_schedule_workbook_downloader():
    schedule_downloader = ScheduleWorkbookUpdater()
    schedule_downloader.update_workbooks()
    assert get_course_workbooks()
