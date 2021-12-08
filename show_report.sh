#!/bin/bash

set -e
PACKAGE_NAME=advanced_logic
pycodestyle --max-doc-length 160 --ignore E402,E203,E501,W503 ${PACKAGE_NAME}
pylint --rcfile=.pylintrc ${PACKAGE_NAME}
mypy --config-file mypy.ini ${PACKAGE_NAME}
pytest --cov ${PACKAGE_NAME} --cov-report term-missing --cov-fail-under=99 \
       --doctest-modules ${PACKAGE_NAME}
scc -i py ${PACKAGE_NAME}
