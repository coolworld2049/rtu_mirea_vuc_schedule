import pathlib
from pathlib import Path
from tempfile import gettempdir

import yaml
from dotenv import load_dotenv
from loguru import logger
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from schedule_service.services.vuc_schedule_parser.parser.schemas import (
    WorkbookFile,
    WorkbookSettings,
)

load_dotenv()

TEMP_DIR = Path(gettempdir())


class ScheduleParserSettings(BaseSettings):
    _worksheets_dir: pathlib.Path | str = pathlib.Path(__file__).parent.parent.joinpath(
        "workbook_updater/files",
    )

    @property
    def worksheets_dir(self):
        return self._worksheets_dir

    @property
    def course_workbooks(self):
        workbooks = []
        for course_dir in self._worksheets_dir.iterdir():
            if not course_dir.is_dir():
                continue
            workbook_path = None
            settings_file = None
            for file in course_dir.iterdir():
                key = None
                if file.suffix in [".xlsx"]:
                    workbook_path = file
                elif file.suffix in [".yml", ".yaml"]:
                    settings_file = file
            try:
                settings = yaml.safe_load(settings_file.open("r", encoding="utf-8"))
                worksheet_settings = {
                    item["name"]: WorkbookSettings(**item["settings"])
                    for item in list(settings.values())[0]
                }
                workbook_file = WorkbookFile(
                    course=int(course_dir.name.split("-")[0]),
                    workbook_path=workbook_path,
                    workbook_settings_path=settings_file,
                    workbook_settings=worksheet_settings,
                )
                workbooks.append(workbook_file)
            except Exception as e:
                logger.error(e)
        return workbooks


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6381
    redis_user: str | None = None
    redis_pass: str | None = None
    redis_base: int | None = None

    @property
    def redis_url(self) -> URL:
        path = "/"
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )


class ScheduleUpdaterSettings(BaseSettings):
    year: int | str | None = None
    month: int | str | None = None
    day: int | str | None = "*/1"
    week: int | str | None = None
    day_of_week: int | str | None = None
    hour: int | str | None = None
    minute: int | str | None = None
    second: int | str | None = None


class Settings(RedisSettings, ScheduleParserSettings, ScheduleUpdaterSettings):
    app_module: str = "schedule_service.web.application:get_app"
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    reload: bool = True
    log_level: str = "DEBUG"
    cors_origins: list[str] | None = ["http://localhost", "http://0.0.0.0"]
    pypi_username: str | None = None
    pypi_password: str | None = None

    _prometheus_dir: Path = TEMP_DIR / "prom"

    @property
    def prometheus_dir(self):
        return self._prometheus_dir

    @field_validator("cors_origins", mode="before", check_fields=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_prefix="SCHEDULE_SERVICE_",
        env_file_encoding="utf-8",
    )


schedule_updater_settings = ScheduleUpdaterSettings()
settings = Settings()
