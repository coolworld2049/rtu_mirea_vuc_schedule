import datetime
import pathlib
import re
from datetime import datetime

from pydantic.main import BaseModel

from schedule_service.services.vuc_schedule_parser.parser.utils import MONTH_MAPPING


class Shape(BaseModel):
    rows: int
    cols: int


class WorkbookSettings(BaseModel):
    day_range: Shape = Shape(rows=14, cols=8)
    year_range: Shape = Shape(rows=2, cols=2)
    days_in_week_column_number: int = 5
    platoon_column_number: int = 2
    subject_rows_number: int = 3

    @property
    def week_range_dim(self):
        return Shape(
            rows=self.days_in_week_column_number * self.day_range.rows,
            cols=self.day_range.cols,
        )

    @property
    def platoon_range_dim(self):
        return Shape(rows=self.day_range.cols + 1, cols=self.platoon_column_number)


class WorkbookFile(BaseModel):
    course: int
    course_dir: pathlib.Path | str
    workbook_path: pathlib.Path
    workbook_settings_path: pathlib.Path
    workbook_settings: dict[str, WorkbookSettings]


class Lesson(BaseModel):
    topic: int
    lesson: int
    type: str


class Subject(BaseModel):
    name: str | None = None
    auditory: str | None = None
    teacher: str | None = None
    lesson: Lesson | None = None

    @staticmethod
    def parse_auditory(value: str):
        if not value:
            return None
        pattern = r"\d+-\d+"
        match = re.search(pattern, value)
        if not match:
            return None
        math_range = match.group().split("-")
        lesson = Lesson(
            topic=int(math_range[0]),
            lesson=int(math_range[1]),
            type=value.split("/")[-1],
        )
        return lesson


class Platoon(BaseModel):
    specialty_code: int
    platoon_number: int | list[int] = []

    @staticmethod
    def parse_platoon_number(platoon_name):
        platoon_number = int(str(platoon_name).split(" ")[0])
        return platoon_number

    @staticmethod
    def parse_speciality_code(platoon_name):
        specialty_code_match = re.search(r"\(([^)]+)\)", platoon_name)
        if not specialty_code_match:
            return None
        specialty_code = int(specialty_code_match.group(1))
        return specialty_code


class WeekSchedule(BaseModel):
    date: str | None = None
    datetime: str | None = None
    subjects: list[Subject] = None
    coordinates: tuple[str, str] = None

    @staticmethod
    def parse_date_raw(date_day_month: str, year_range: tuple[int, int] = None):
        day, month = date_day_month.split(" ")
        month = MONTH_MAPPING.get(month)
        date = f"{day}-{month}"
        if year_range:
            year = year_range[0] if month < 12 else year_range[1]
            date += f"-{datetime.now().year}"
        return date

    @staticmethod
    def parsed_date_range(date_day_month: str):
        day_month_str = WeekSchedule.parse_date_raw(date_day_month)
        spl = day_month_str.split("-")
        return [int(x) for x in spl]


class Day(BaseModel):
    day: str
    platoons: list[int]


class DayResult(BaseModel):
    week: int
    days: list[Day] = []


class WeekScheduleResult(BaseModel):
    platoon: Platoon
    schedule: WeekSchedule


class ScheduleResult(BaseModel):
    week: int
    schedule: list[WeekScheduleResult]
