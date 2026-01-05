import pytest
from rest_framework.test import APIClient

from booking.models import Room

pytestmark = pytest.mark.django_db


def test_rooms_create_success():
    client = APIClient()
    resp = client.post(
        "/rooms/create", {"description": "room", "price_per_night": 1000}, format="multipart"
    )
    assert resp.status_code == 200
    assert "room_id" in resp.json()
    room_id = resp.json()["room_id"]
    room = Room.objects.get(id=room_id)
    assert room.description == "room"
    assert room.price_per_night == 1000


@pytest.mark.parametrize(
    "payload,expected_error",
    [
        ({"description": "", "price_per_night": 100}, "description is required"),
        ({"description": " ", "price_per_night": 100}, "description is required"),
        ({"description": "aa", "price_per_night": "aa"}, "price_per_night must be an integer"),
        ({"description": "aa", "price_per_night": 0}, "price_per_night must be > 0"),
        ({"description": "aa", "price_per_night": -1}, "price_per_night must be > 0"),
    ],
)
def test_rooms_create_validation_errors(payload, expected_error):
    client = APIClient()
    resp = client.post("/rooms/create", payload, format="multipart")
    assert resp.status_code == 400
    assert resp.json()["error"] == expected_error


def test_rooms_list_default_sort_created_at_desc():
    client = APIClient()
    r1 = Room.objects.create(description="old", price_per_night=100)
    r2 = Room.objects.create(description="new", price_per_night=200)
    resp = client.get("/rooms/list")
    assert resp.status_code == 200
    data = resp.json()
    assert [r["room_id"] for r in data] == [r2.id, r1.id]


def test_rooms_list_sort_price_asc():
    client = APIClient()
    r1 = Room.objects.create(description="cheap", price_per_night=100)
    r2 = Room.objects.create(description="expensive", price_per_night=300)
    resp = client.get("/rooms/list?sort_by=price&order=asc")
    assert resp.status_code == 200
    data = resp.json()
    assert [r["room_id"] for r in data] == [r1.id, r2.id]


def test_rooms_list_invalid_sort_params():
    client = APIClient()
    resp = client.get("/rooms/list?sort_by=bad")
    assert resp.status_code == 400
    assert "sort_by must be" in resp.json()["error"]

    resp = client.get("/rooms/list?order=bad")
    assert resp.status_code == 400
    assert "order must be" in resp.json()["error"]
