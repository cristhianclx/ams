#!/bin/bash

black . --check
pylint -j 0 app data
flake8 app data
mypy app data

rm -f tests.db

pytest -v \
  --cov  \
  --no-cov-on-fail
