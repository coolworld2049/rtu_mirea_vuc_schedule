from fastapi import Query
from pydantic.main import BaseModel


class ScheduleParams(BaseModel):
    course: int = Query(...)
    week: int | None = Query(None)
    platoon: int | None = Query(None)
