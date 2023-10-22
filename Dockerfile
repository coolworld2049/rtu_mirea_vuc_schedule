FROM python:3.11.6-slim-bullseye as build

RUN pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install

COPY . /app/

RUN poetry install


FROM build as workbook_updater

RUN pytest workbook_updater

CMD ["python", "-m", "workbook_updater"]


FROM build as schedule_service

RUN pytest schedule_service

CMD ["python", "-m", "schedule_service"]
