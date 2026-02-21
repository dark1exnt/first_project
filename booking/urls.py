from django.urls import path

from booking import views

urlpatterns = [
    path("health/", views.health),
    path("rooms/", views.rooms),
    path("rooms/<int:room_id>/", views.rooms_delete),
    path("bookings/", views.bookings),
    path("bookings/<int:booking_id>/", views.bookings_delete),
]
