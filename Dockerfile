FROM python:3.11.6-slim-bullseye as build

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install -n

COPY . /app/

FROM build as workbook_updater

RUN pytest workbook_updater

CMD ["python", "-m", "workbook_updater"]

FROM build as schedule_service

RUN pytest schedule_service

CMD ["python", "-m", "schedule_service"]
