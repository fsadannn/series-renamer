PROJECT=series_renamer

.PHONY: install-poetry
install-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	# for windows comment the line above and uncomment the next line, for powershell only the next line
	# powershell "(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python"
	poetry install

.PHONY: install-packages
install-packages:
	poetry install

.PHONY: update-packages
update:
	poetry update

.PHONY: lock
lock:
	poetry lock

.PHONY: sync-version
sync-version:
	poetry run python sync-version.py

.PHONY: build
build: sync-version
	poetry build

.PHONY: lint
lint: sync-version
	poetry run pylint ${PROJECT} -f colorized -d missing-module-docstring,missing-class-docstring,missing-function-docstring,invalid-name

.PHONY: test
test: sync-version
	poetry run pytest ${PROJECT} tests --doctest-modules --cov=${PROJECT} --cov-report=xml --cov-config=.coveragerc -v

.PHONY: test-fast
test-fast: sync-version
	poetry run pytest ${PROJECT} tests -v

.PHONY: cov
cov: sync-version
	poetry run codecov