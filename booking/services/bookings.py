from __future__ import annotations

from datetime import date

from django.http import Http404

from booking.models import Booking, Room


def create_booking(*, room_id: int, date_start: date, date_end: date) -> int:
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist as exc:
        raise Http404("room not found") from exc

    booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
    return booking.id


def list_bookings(*, room_id: int) -> list[Booking]:
    if not Room.objects.filter(id=room_id).exists():
        raise Http404("room not found")

    return list(Booking.objects.filter(room_id=room_id).order_by("date_start", "id"))


def delete_booking(*, booking_id: int) -> None:
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist as exc:
        raise Http404("booking not found") from exc
    booking.delete()
