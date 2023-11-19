VENV_NAME?=.venv
PYTHON_VERSION?=3.11

venv-create:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	pip install poetry
	poetry install

venv-activate:
	. $(VENV_NAME)/bin/activate

venv-clean:
	rm -rf $(VENV_NAME)

source:
	source $(PWD)/.env.sh &&

reset-db:
	source $(PWD)/.env.sh && \
	python3 -m src reset-db

run-local:
	source $(PWD)/.env.sh && \
	uvicorn src.main:create_app --factory --reload --log-config=./config/log_conf.yaml

clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info/

lint:
	poetry run black . && \
	poetry run isort .

ruff:
	poetry run ruff $(SRC) --fix .

pyright:
	poetry run pyright $(SRC) .

test:
	source $(PWD)/.env.sh && \
	poetry run pytest

coverage:
	coverage run --rcfile ./pyproject.toml -m pytest ./tests && \
	coverage report --fail-under 95


docker-prod:
	DOCKER_BUILDKIT=0 docker build -t poetry-project .
