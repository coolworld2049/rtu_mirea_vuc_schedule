from json import JSONDecodeError
from typing import Callable

from fastapi import HTTPException
from fastapi import Query

from schedule_service.web.api.v1.schedule.schemas import ScheduleParams


def schedule_params(
    course: dict = None,
    week: dict = None,
    platoon: dict = None,
) -> Callable[[int | None, int | None, int | None, int | None], ScheduleParams]:
    _course = {"default": ..., "examples": [4]}
    _week = {"default": None, "examples": [8]}
    _platoon = {"default": None, "examples": [222]}

    _course.update(**course) if course else None
    _week.update(**week) if week else None
    _platoon.update(**platoon) if platoon else None

    def inner(
        course_: int = Query(
            alias="course",
            enum=list(range(3, 6)),
            **_course,
        ),
        week_: int
        | None = Query(
            alias="week",
            enum=list(range(1, 19)),
            **_week,
        ),
        platoon_: int
        | None = Query(
            alias="platoon",
            **_platoon,
        ),
    ):
        try:
            schedule_params = ScheduleParams(
                course=course_,
                week=week_,
                platoon=platoon_,
            )
            return schedule_params
        except JSONDecodeError:
            raise HTTPException(400, f"Invalid query params")

    return inner
