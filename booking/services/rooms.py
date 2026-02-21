from __future__ import annotations

from typing import Literal

from django.http import Http404

from booking.models import Room

SortBy = Literal["price", "created_at"]
Order = Literal["asc", "desc"]


def create_room(*, description: str, price_per_night: int) -> int:
    room = Room.objects.create(description=description, price_per_night=price_per_night)
    return room.id


def list_rooms(*, sort_by: SortBy = "created_at", order: Order = "desc") -> list[Room]:
    field = "price_per_night" if sort_by == "price" else "created_at"

    ordering = field if order == "asc" else f"-{field}"

    return list(Room.objects.all().order_by(ordering))


def delete_room(*, room_id: int) -> None:
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist as exc:
        raise Http404("room not found") from exc
    room.delete()
