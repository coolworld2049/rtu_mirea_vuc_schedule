from cashews import cache
from fastapi import APIRouter
from fastapi.params import Depends

from schedule_service.services.vuc_schedule_parser.dependency import (
    get_workbook_parsers,
)
from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser
from schedule_service.services.vuc_schedule_parser.parser.schemas import (
    Platoon,
    ScheduleResult,
    WeekDate,
    WeekScheduleResult,
)
from schedule_service.settings import settings
from schedule_service.web.api.v1.schedule.params import schedule_params
from schedule_service.web.api.v1.schedule.schemas import ScheduleParams

router = APIRouter()

key_template = ":params:{params}"
cache.setup(settings.redis_url.__str__(), db=0)


@router.get("/", response_model=list[ScheduleResult])
@cache(ttl="1d", prefix="get_schedule", key=key_template)
async def get_schedule(
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
        ),
    ),
    workbooks: dict[int, ScheduleParser] = Depends(get_workbook_parsers),
) -> list[ScheduleResult]:
    schedule_parser = workbooks.get(params.course)
    schedule = schedule_parser.parse_all_schedule(
        **params.model_dump(exclude_none=True)
    )
    return schedule


@router.get("/week", response_model=list[WeekScheduleResult])
@cache(ttl="1d", prefix="get_weeks_schedule", key=key_template)
async def get_week_schedule(
    params: ScheduleParams = Depends(schedule_params(week={"default": ...})),
    workbooks: dict[int, ScheduleParser] = Depends(get_workbook_parsers),
) -> list[WeekScheduleResult]:
    schedule_parser = workbooks.get(params.course)
    schedule = schedule_parser.parse_schedule(**params.model_dump(exclude_none=True))
    return schedule


@router.get("/day/week", response_model=list[WeekDate])
@cache(ttl="1d", prefix="get_days_week", key=key_template)
async def get_days_week(
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
            platoon={"default": None},
        ),
    ),
    workbooks: dict[int, ScheduleParser] = Depends(get_workbook_parsers),
) -> list[WeekDate]:
    schedule_parser = workbooks.get(params.course)
    weeks = schedule_parser.get_days_week(**params.model_dump(exclude_none=True))
    return weeks


@router.get("/platoons", response_model=list[Platoon])
@cache(
    ttl="1d",
    prefix="get_weeks_schedule",
    key=key_template + ":speciality_code:{speciality_code}",
)
async def get_platoons(
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
            platoon={"include_in_schema": False},
        ),
    ),
    speciality_code: int = None,
    workbooks: dict[int, ScheduleParser] = Depends(get_workbook_parsers),
) -> list[Platoon]:
    schedule_parser = workbooks.get(params.course)
    platoons = schedule_parser.platoons(speciality_code)
    return platoons
