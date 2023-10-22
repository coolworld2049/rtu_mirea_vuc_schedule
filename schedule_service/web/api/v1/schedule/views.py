# noinspection PyProtectedMember
from cashews import cache
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from schedule_service.services.vuc_schedule_parser.dependency import get_schedule_parser
from schedule_service.services.vuc_schedule_parser.parser.schemas import (
    Platoon,
    ScheduleResult,
    WeekDate,
    WeekScheduleResult,
)
from schedule_service.web.api.v1.schedule.params import schedule_params
from schedule_service.web.api.v1.schedule.schemas import ScheduleParams

router = APIRouter()
cache_key = "params:{params}"


@router.get("/", response_model=list[ScheduleResult])
@cache(
    ttl="1d",
    prefix="get_schedule",
    key=cache_key,
    tags=["schedule"],
)
async def get_schedule(
    request: Request,
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
        ),
    ),
) -> list[ScheduleResult]:
    schedule_parser = get_schedule_parser(request, params.course)
    schedule = schedule_parser.parse_all_schedule(
        **params.model_dump(exclude_none=True)
    )
    return schedule


@router.get("/week", response_model=list[WeekScheduleResult])
@cache(
    ttl="1d",
    prefix="get_weeks_schedule",
    key=cache_key,
    tags=["schedule"],
)
async def get_week_schedule(
    request: Request,
    params: ScheduleParams = Depends(schedule_params(week={"default": ...})),
) -> list[WeekScheduleResult]:
    schedule_parser = get_schedule_parser(request, params.course)
    schedule = schedule_parser.parse_schedule(**params.model_dump(exclude_none=True))
    return schedule


@router.get("/day/week", response_model=list[WeekDate])
@cache(
    ttl="1d",
    prefix="get_days_week",
    key=cache_key,
)
async def get_days_week(
    request: Request,
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
            platoon={"default": None},
        ),
    ),
) -> list[WeekDate]:
    schedule_parser = get_schedule_parser(request, params.course)
    weeks = schedule_parser.get_days_week(**params.model_dump(exclude_none=True))
    return weeks


@router.get("/platoons", response_model=list[Platoon])
@cache(
    ttl="1d",
    prefix="get_weeks_schedule",
    key=cache_key + ":speciality_code:{speciality_code}",
)
async def get_platoons(
    request: Request,
    params: ScheduleParams = Depends(
        schedule_params(
            week={"include_in_schema": False},
            platoon={"include_in_schema": False},
        ),
    ),
    speciality_code: int = None,
) -> list[Platoon]:
    schedule_parser = get_schedule_parser(request, params.course)
    platoons = schedule_parser.platoons(speciality_code)
    return platoons
