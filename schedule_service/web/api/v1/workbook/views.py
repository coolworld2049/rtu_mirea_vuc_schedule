from datetime import datetime

from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from schedule_service.services.vuc_schedule_parser.parser.schemas import WorkbookFile
from schedule_service.settings import settings

router = APIRouter()


@router.get("/", response_model=list[WorkbookFile] | WorkbookFile)
async def get_workbooks(
    course: int | None = None,
) -> list[WorkbookFile] | WorkbookFile:
    if course:
        wb = [x for x in settings.workbook_files if x.course == course]
        if len(wb) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return wb[0]
    return settings.workbook_files


@router.get(
    "/relevance",
    response_model=str,
    description="Returns datetime string",
)
async def get_workbook_relevance(
    course: int,
) -> str:
    wb = [x for x in settings.workbook_files if x.course == course]
    if len(wb) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    st_mtime = wb[0].workbook_path.stat().st_mtime
    st_date = datetime.fromtimestamp(st_mtime).strftime("%d-%m-%Y")
    return st_date
