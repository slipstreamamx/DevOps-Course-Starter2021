FROM python:3.9-slim-buster as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

WORKDIR /app

COPY poetry.lock pyproject.toml /app

RUN pip3 install poetry

EXPOSE 5001

RUN poetry install

COPY ./todo_app /app/todo_app

FROM base as development

ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "--port", "5001"]