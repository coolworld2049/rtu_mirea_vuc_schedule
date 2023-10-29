FROM python:3.11.6-slim-bullseye as rtu_mirea_vuc_schedule

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install -n

COPY . /app/
