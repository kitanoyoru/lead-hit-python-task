# LeadHit Junior+ Python task

## Installation

### Locally

This project contains my version of the solution on LeadHit task on the Junior+ Python Developper

## Installation

### Locally

Import data in your database using [mongoimport](https://www.mongodb.com/docs/database-tools/mongoimport). Data could be find in /data folder, it looks smth like this

```sh

# formTemplateCollection
{"_id":{"$oid":"655bf3fa97483dedc59b221a"},"name":"FirstForm","field_1":"EMAIL","field_2":"TEXT","field_3":"DATE"}
{"_id":{"$oid":"655bf43097483dedc59b221b"},"name":"SecondForm","field_4":"EMAIL","field_5":"PHONE"}
```

Write your creds in .env.sh file in the root folder. Here is an example:

```
# Project structure

├── .env.sh
├── .git
├── .gitignore
├── .pre-commit-config.yaml
├── .ruff_cache
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── config
├── data
├── docker
├── poetry.lock
├── pyproject.toml
├── scripts
├── src
└── tests

# .env.sh

export DATABASE_URL="user:password@localhost:27017"
export DATABASE_NAME="test"

```

Install needed dependencies and start server:

```sh
poetry install && make run-local

```

### In Docker (In Dev now, but it will be done soon)

```sh
./scripts/start_compose.sh
```
