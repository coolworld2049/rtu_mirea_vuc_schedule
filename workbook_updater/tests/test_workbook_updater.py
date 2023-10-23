from workbook_updater.__main__ import ScheduleWorkbookUpdater

from schedule_service.services.vuc_schedule_parser.lifetime import get_workbook_parsers


def test_schedule_workbook_downloader():
    schedule_downloader = ScheduleWorkbookUpdater()
    schedule_downloader.update_workbooks()
    assert get_workbook_parsers()
