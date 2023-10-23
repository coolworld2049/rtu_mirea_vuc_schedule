from typing import Callable

from fastapi import Query
from pydantic import BaseModel


class ScheduleParams(BaseModel):
    course: int
    week: int | None = None
    platoon: int | None = None


def schedule_params(
    course: dict = None,
    week: dict = None,
    platoon: dict = None,
) -> Callable[[int, int | None, int | None], ScheduleParams]:
    _course = {"default": ..., "example": 4}
    _week = {"default": None, "example": 8}
    _platoon = {"default": None, "example": 222}

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
        course_dir = f"{course_}-course"
        schedule_params = ScheduleParams(
            course=course_,
            week=week_,
            platoon=platoon_,
        )
        return schedule_params

    return inner
