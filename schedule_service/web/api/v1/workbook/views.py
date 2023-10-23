from datetime import datetime

# noinspection PyProtectedMember
from cashews import cache
from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from schedule_service.services.vuc_schedule_parser.parser.schemas import WorkbookFile
from schedule_service.settings import settings

router = APIRouter()
key_template = "course:{course}"
cache.setup(settings.redis_url.__str__(), db=1)


@router.get("/", response_model=list[WorkbookFile])
async def get_workbooks() -> list[WorkbookFile]:
    return settings.workbook_files


@router.get("/{course}", response_model=WorkbookFile)
async def get_course_workbook(
    course: int,
) -> WorkbookFile:
    wb = [x for x in settings.workbook_files if x.course == course]
    if len(wb) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return wb[0]


@router.get(
    "/relevance/{course}",
    response_model=str,
    description="Returns datetime string",
)
@cache(
    ttl="720m",
    prefix="get_course_workbook_relevance",
    key=key_template,
)
async def get_course_workbook_relevance(
    course: int,
) -> str:
    wb = [x for x in settings.workbook_files if x.course == course]
    if len(wb) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    st_mtime = wb[0].workbook_path.stat().st_mtime
    st_date = datetime.fromtimestamp(st_mtime).strftime("%d-%m-%Y")
    return st_date
