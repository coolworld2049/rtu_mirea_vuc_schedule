from schedule_service.services.vuc_schedule_parser.lifetime import (
    get_workbook_parsers,
    init_vuc_schedule_parser,
)
from schedule_service.services.vuc_schedule_parser.workbook_updater.base import (
    WorkbookUpdater,
)


def test_workbook_updater(fastapi_app):
    workbook_updater = WorkbookUpdater()
    workbook_updater.update_workbooks(init_vuc_schedule_parser, fastapi_app)
    assert get_workbook_parsers()
