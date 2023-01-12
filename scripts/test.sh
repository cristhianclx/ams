#!/bin/bash

black app/ data/ --check --diff --color --line-length 120
autoflake --check --remove-unused-variables --remove-all-unused-imports -r app/ data/
isort app/ data/ --diff --color --profile black
pylint -j 0 app/ data/
flake8 app/ data/
mypy app/ data/

rm -f tests.db

SQLALCHEMY_SILENCE_UBER_WARNING=1 pytest -v \
  --cov  \
  --no-cov-on-fail
