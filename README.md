# first_project



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

## API methods

### Rooms
`POST /rooms/create`
`GET /rooms/list?sort_by=price|created_at&order=asc|desc`
`POST /rooms/delete`

### Bookings
`POST /bookings/create`
`GET /bookings/list?room_id=...`
`POST /bookings/delete`
