FROM python:3.9-slim-buster as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

WORKDIR /app

COPY poetry.lock pyproject.toml /app

RUN pip3 install poetry

EXPOSE 5001

RUN poetry install

COPY ./todo_app /app/todo_app

FROM base as development
EXPOSE 5001
# run flask via a shell script for dev work
CMD ["./docker_entrypoint_launch.sh"]