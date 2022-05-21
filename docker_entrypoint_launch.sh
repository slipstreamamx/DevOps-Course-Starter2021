#!/bin/sh

cd /usr/src

$HOME/.poetry/bin/poetry run flask run --host=0.0.0.0
