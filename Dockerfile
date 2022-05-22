FROM python:3.9-slim-buster as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

WORKDIR /app

COPY poetry.lock pyproject.toml /app

RUN pip3 install poetry

EXPOSE 5001

RUN poetry install

COPY ./todo_app /app/todo_app

FROM base as development

COPY docker-entrypoint-dev.sh /app

ENTRYPOINT ["./docker-entrypoint-dev.sh"]

FROM base as production

COPY docker-entrypoint-prod.sh /app
RUN chmod +x /var/log

ENTRYPOINT ["./docker-entrypoint-prod.sh"]
