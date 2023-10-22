FROM python:3.11.6-slim-bullseye as prod

RUN pip install poetry==1.4.8

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install --only main

COPY . /app/

RUN poetry install --only main

CMD ["/bin/bash", "./start.sh"]

FROM prod as dev

RUN poetry install

FROM prod as workbook_updater

CMD ["python", "-m", "schedule_service.services.workbook_updater"]
