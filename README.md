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
cp .env.example .env
docker compose up --build
```

## API methods

### Rooms
**Create room**
`POST /rooms/`
JSON:
```JSON
{
    "description": "some_text",
    "price_per_night": 1000
}
```

**List rooms**
`GET /rooms/?sort_by=price|created_at&order=asc|desc`

**Delete room**
`DELETE /rooms/{room_id}`

### Bookings
**Create booking**
`POST /bookings/`
JSON:
```JSON
{
    "room_id": 1,
    "date_start: "2026-01-10",
    "date_end": "2026-01-12"
}
```

**List bookings**
`GET /bookings/?room_id={room_id}`

**Delete booking**
`DELETE /bookings/{booking_id}`
