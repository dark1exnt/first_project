# first_project

Первый проект.


## Stack
- Python 3.12
- Django, Django REST Framework
- PostgreSQL
- Poetry
- Docker, docker-compose
- Ruff, pre-commit

## Run project
```bash
docker compose up -d
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:9000
```
