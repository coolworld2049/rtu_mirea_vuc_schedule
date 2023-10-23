from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    year: int | str | None = None
    month: int | str | None = None
    day: int | str | None = "*/1"
    week: int | str | None = None
    day_of_week: int | str | None = None
    hour: int | str | None = None
    minute: int | str | None = None
    second: int | str | None = None


settings = Settings()
