from datetime import date

import pytest
from rest_framework.test import APIClient

from booking.models import Booking, Room

pytestmark = pytest.mark.django_db


def test_bookings_create_success_and_list_sorted():
    client = APIClient()
    room = Room.objects.create(description="room", price_per_night=100)

    b1 = client.post(
        "/bookings/create",
        {"room_id": room.id, "date_start": "2026-01-10", "date_end": "2026-01-12"},
        format="multipart",
    )
    assert b1.status_code == 200
    booking_id_1 = b1.json()["booking_id"]
    b2 = client.post(
        "/bookings/create",
        {"room_id": room.id, "date_start": "2026-01-05", "date_end": "2026-01-06"},
        format="multipart",
    )
    assert b2.status_code == 200
    booking_id_2 = b2.json()["booking_id"]

    resp = client.get(f"/bookings/list?room_id={room.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert [b["booking_id"] for b in data] == [booking_id_2, booking_id_1]


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        (
            {"room_id": "abc", "date_start": "2026-01-10", "date_end": "2026-01-12"},
            "room id must be an integer",
        ),
        ({"room_id": 999, "date_start": "2026-01-10", "date_end": "2026-01-12"}, "room not found"),
        (
            {"room_id": 1, "date_start": "bad", "date_end": "2026-01-12"},
            "date_start must be a string in YYYY-MM-DD format",
        ),
        (
            {"room_id": 1, "date_start": "2026-01-10", "date_end": "bad"},
            "date_end must be a string in YYYY-MM-DD format",
        ),
        (
            {"room_id": 1, "date_start": "2026-01-10", "date_end": "2026-01-10"},
            "date_end must be greater than date_start",
        ),
    ],
)
def test_bookings_create_validation_errors(payload, expected_error):
    client = APIClient()
    room = Room.objects.create(description="room", price_per_night=1000)
    if payload.get("room_id") == 1:
        payload = {**payload, "room_id": room.id}
    resp = client.post("/bookings/create", payload, format="multipart")

    if expected_error == "room not found":
        assert resp.status_code == 404
    else:
        assert resp.status_code == 400
    assert expected_error in resp.json()["error"]


def test_bookings_rejects_overlap():
    client = APIClient()
    room = Room.objects.create(description="room", price_per_night=1000)

    resp = client.post(
        "/bookings/create",
        {"room_id": room.id, "date_start": "2026-01-10", "date_end": "2026-01-12"},
        format="multipart",
    )
    assert resp.status_code == 200
    resp2 = client.post(
        "/bookings/create",
        {"room_id": room.id, "date_start": "2026-01-11", "date_end": "2026-01-13"},
        format="multipart",
    )
    assert resp2.status_code == 400
    assert resp2.json()["error"] == "room is not available for selected dates"


def test_bookings_delete_success_and_not_found():
    client = APIClient()
    room = Room.objects.create(description="room", price_per_night=1000)
    booking = Booking.objects.create(
        room=room, date_start=date(2026, 1, 10), date_end=date(2026, 1, 12)
    )

    resp = client.post("/bookings/delete", {"booking_id": booking.id}, format="multipart")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert not Booking.objects.filter(id=booking.id).exists()

    resp2 = client.post("/bookings/delete", {"booking_id": booking.id}, format="multipart")
    assert resp2.status_code == 404
    assert resp2.json()["error"] == "booking not found"


def test_rooms_delete_cascades_bookings():
    client = APIClient()
    room = Room.objects.create(description="room", price_per_night=1000)
    booking = Booking.objects.create(
        room=room, date_start=date(2026, 1, 10), date_end=date(2026, 1, 12)
    )

    resp = client.post("/rooms/delete", {"room_id": room.id}, format="multipart")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert not Room.objects.filter(id=room.id).exists()
    assert not Booking.objects.filter(id=booking.id).exists()
