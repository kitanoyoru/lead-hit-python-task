FROM python:3.11-slim-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder-base

RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        vim \
        netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.6.1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main

FROM python-base as development

ENV FASTAPI_ENV=development

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@

CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--factory", "--log-config=./config/log_conf.yaml", "src.main:create_app"]

FROM development AS lint

RUN black --config ./pyproject.toml --check src tests
RUN isort --settings-path ./pyproject.toml --check-only src tests

CMD ["tail", "-f", "/dev/null"]

FROM development AS test

RUN poetry run pytest
#RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests
#RUN coverage report --fail-under 50

FROM python-base AS production

ENV FASTAPI_ENV=production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY config/gunicorn_conf.py /gunicorn_conf.py

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create user with the name poetry
RUN groupadd -g 1500 poetry && \
    useradd -m -u 1500 -g poetry poetry

COPY --chown=poetry:poetry ./src /app

USER poetry
WORKDIR /app

ENTRYPOINT /docker-entrypoint.sh $0 $@

CMD ["gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py", "src.main:create_app"]

