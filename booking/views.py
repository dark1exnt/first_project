from __future__ import annotations

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from booking.services.rooms import create_room, delete_room, list_rooms


def _error(message: str, http_status: int) -> Response:
    return Response({"error": message}, status=http_status)


@api_view(["POST"])
def rooms_create(request):
    description = request.data.get("description")
    price_per_night = request.data.get("price_per_night")

    if not isinstance(description, str) or not description.strip():
        return _error("description is required", status.HTTP_400_BAD_REQUEST)

    try:
        price_per_night_int = int(price_per_night)
    except (TypeError, ValueError):
        return _error("price_per_night must be an integer", status.HTTP_400_BAD_REQUEST)

    if price_per_night_int <= 0:
        return _error("price_per_night must be > 0", status.HTTP_400_BAD_REQUEST)

    room_id = create_room(description=description.strip(), price_per_night=price_per_night_int)
    return Response({"room_id": room_id}, status=status.HTTP_200_OK)


@api_view(["GET"])
def rooms_list(request):
    sort_by = request.query_params.get("sort_by", "created_at")
    order = request.query_params.get("order", "desc")

    if sort_by not in {"price", "created_at"}:
        return _error("sort_by must be 'price' or 'created_at'", status.HTTP_400_BAD_REQUEST)

    if order not in {"asc", "desc"}:
        return _error("order must be 'asc' or 'desc'", status.HTTP_400_BAD_REQUEST)

    rooms = list_rooms(sort_by=sort_by, order=order)

    data = [
        {
            "room_id": r.id,
            "description": r.description,
            "price_per_night": r.price_per_night,
            "created_at": r.created_at.isoformat(),
        }
        for r in rooms
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def rooms_delete(request):
    room_id = request.data.get("room_id")
    try:
        room_id_int = int(room_id)
    except (TypeError, ValueError):
        return _error("room_id must be integer", status.HTTP_400_BAD_REQUEST)

    try:
        delete_room(room_id=room_id_int)
    except Http404:
        return _error("room not found", status.HTTP_404_NOT_FOUND)

    return Response({"status": "ok"}, status=status.HTTP_200_OK)
