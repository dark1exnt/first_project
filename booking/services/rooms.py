from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from booking.models import Room


SortBy = Literal["price", "created_at"]
Order = Literal["asс", "desc"]


def create_room(*, description: str, price_per_night: int) -> int:
    room = Room.objects.create(description=description, price_per_night=price_per_night)
    return room.id

def list_rooms(*, sort_by: SortBy = "created_at", order: Order = "desc") -> list[Room]:
    if sort_by == "price":
        field = "price_per_night"
    else:
        field = "created_at"

    if order == "asc":
        ordering = field
    else:
        ordering = f"-{field}"
    
    return list(Room.objects.all().order_by(ordering))