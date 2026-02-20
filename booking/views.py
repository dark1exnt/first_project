from __future__ import annotations

from datetime import date

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from booking.services.bookings import create_booking, delete_booking, list_bookings
from booking.services.rooms import create_room, delete_room, list_rooms


def _error(message: str, http_status: int) -> Response:
    return Response({"error": message}, status=http_status)


def _parse_date(value: object, field_name: str) -> tuple[date | None, Response | None]:
    if not isinstance(value, str):
        return None, _error(
            f"{field_name} must be a string in YYYY-MM-DD format", status.HTTP_400_BAD_REQUEST
        )
    try:
        return date.fromisoformat(value), None
    except ValueError:
        return None, _error(
            f"{field_name} must be a string in YYYY-MM-DD format", status.HTTP_400_BAD_REQUEST
        )


def _rooms_create(request):
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
    return Response({"room_id": room_id}, status=status.HTTP_201_CREATED)


def _rooms_list(request):
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


def _bookings_create(request):
    room_id = request.data.get("room_id")
    date_start_raw = request.data.get("date_start")
    date_end_raw = request.data.get("date_end")

    try:
        room_id_int = int(room_id)
    except (TypeError, ValueError):
        return _error("room id must be an integer", status.HTTP_400_BAD_REQUEST)

    date_start, err = _parse_date(date_start_raw, "date_start")
    if err:
        return err

    date_end, err = _parse_date(date_end_raw, "date_end")
    if err:
        return err

    if date_end <= date_start:
        return _error("date_end must be greater than date_start", status.HTTP_400_BAD_REQUEST)

    try:
        booking_id = create_booking(room_id=room_id_int, date_start=date_start, date_end=date_end)
    except Http404:
        return _error("room not found", status.HTTP_404_NOT_FOUND)
    except ValueError:
        return _error("room is not available for selected dates", status.HTTP_400_BAD_REQUEST)

    return Response({"booking_id": booking_id}, status=status.HTTP_201_CREATED)


def _bookings_list(request):
    room_id = request.query_params.get("room_id")

    try:
        room_id_int = int(room_id)
    except (TypeError, ValueError):
        return _error("room id must be an integer", status.HTTP_400_BAD_REQUEST)

    try:
        bookings = list_bookings(room_id=room_id_int)
    except Http404:
        return _error("room not found", status.HTTP_404_NOT_FOUND)

    data = [
        {
            "booking_id": b.id,
            "date_start": b.date_start.isoformat(),
            "date_end": b.date_end.isoformat(),
        }
        for b in bookings
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def rooms(request):
    if request.method == "GET":
        return _rooms_list(request)

    if request.method == "POST":
        return _rooms_create(request)


@api_view(["DELETE"])
def rooms_delete(request, room_id: int):
    try:
        delete_room(room_id=room_id)
    except Http404:
        return _error("room not found", status.HTTP_404_NOT_FOUND)

    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def bookings(request):
    if request.method == "GET":
        return _bookings_list(request)

    if request.method == "POST":
        return _bookings_create(request)


@api_view(["DELETE"])
def bookings_delete(request, booking_id: int):
    try:
        delete_booking(booking_id=booking_id)
    except Http404:
        return _error("booking not found", status.HTTP_404_NOT_FOUND)

    return Response({"status": "ok"}, status=status.HTTP_200_OK)
