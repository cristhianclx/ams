#!/bin/bash

black . --check --diff --color --line-length 120
autoflake --check --remove-unused-variables --remove-all-unused-imports -r .
isort . --diff --color --profile black
pylint -j 0 app/
flake8 app/
mypy app/

rm -f tests.db

pytest -v \
  --cov  \
  --no-cov-on-fail
