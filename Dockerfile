FROM python:3.8-slim-buster as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

WORKDIR /app

RUN pip3 install poetry

COPY poetry.lock pyproject.toml /app/

EXPOSE 5001

RUN poetry config virtualenvs.create false --local && poetry install

COPY ./todo_app /app/todo_app

FROM base as development

COPY docker-entrypoint-dev.sh /app

ENTRYPOINT ["./docker-entrypoint-dev.sh"]

FROM base as production

COPY docker-entrypoint-prod.sh /app

ENTRYPOINT ["./docker-entrypoint-prod.sh"]

FROM base as testing
EXPOSE 5002
COPY docker-entrypoint-testing.sh /app
COPY ./tests /app/tests
ENTRYPOINT ["./docker-entrypoint-testing.sh"]
