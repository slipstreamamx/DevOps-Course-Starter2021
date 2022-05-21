FROM python:3.9-slim-buster as base

RUN mkdir -p /usr/src/todo_app

COPY . /usr/src/todo_app

WORKDIR /usr/src/tod_app

RUN apt update -y &&\ 
    apt install curl -y &&\
    curl -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py &&\
    chmod +x get-poetry.py &&\ 
    python get-poetry.py &&\
    . $HOME/.poetry/env\
    $HOME/.poetry/bin/poetry install --no-interaction

ENV PATH="$HOME/.poetry/bin:$PATH"

ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "--port", "5001"]