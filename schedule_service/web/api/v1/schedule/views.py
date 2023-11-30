from cashews import cache
from fastapi import APIRouter
from fastapi.params import Depends

from schedule_service.services.vuc_schedule_parser.dependency import (
    get_workbook_parsers,
)
from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser
from schedule_service.services.vuc_schedule_parser.parser.schemas import (
    DayResult,
    Platoon,
    ScheduleResult,
    WeekScheduleResult,
)
from schedule_service.web.api.v1.schedule.params import ScheduleParams, schedule_params

router = APIRouter()


@router.get("/", response_model=list[ScheduleResult])
@cache(ttl="1d", lock=True)
async def get_schedule(
    params: ScheduleParams = Depends(
        schedule_params(week={"include_in_schema": False}),
    ),
    schedule_parser: ScheduleParser = Depends(get_workbook_parsers),
) -> list[ScheduleResult]:
    schedule = schedule_parser.parse_all_schedule(
        **params.model_dump(exclude_none=True)
    )
    return schedule


@router.get("/week", response_model=list[WeekScheduleResult])
@cache(ttl="1d", lock=True)
async def get_week_schedule(
    params: ScheduleParams = Depends(schedule_params(week={"default": ...})),
    schedule_parser: ScheduleParser = Depends(get_workbook_parsers),
) -> list[WeekScheduleResult]:
    schedule = schedule_parser.parse_schedule(**params.model_dump(exclude_none=True))
    return schedule


@router.get("/daily", response_model=list[DayResult])
@cache(ttl="1d", lock=True)
async def get_days_week(
    params: ScheduleParams = Depends(
        schedule_params(week={"include_in_schema": False}, platoon={"default": None}),
    ),
    schedule_parser: ScheduleParser = Depends(get_workbook_parsers),
) -> list[DayResult]:
    weeks = schedule_parser.get_days_week(**params.model_dump(exclude_none=True))
    return weeks


@router.get("/platoons", response_model=list[Platoon])
@cache(ttl="1d", lock=True)
async def get_platoons(
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
            platoon={"include_in_schema": False},
        ),
    ),
    schedule_parser: ScheduleParser = Depends(get_workbook_parsers),
    speciality_code: int = None,
) -> list[Platoon]:
    platoons = schedule_parser.platoons(speciality_code)
    return platoons
