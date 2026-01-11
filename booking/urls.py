from django.urls import path

from booking import views

urlpatterns = [
    path("rooms/", views.rooms),
    path("rooms/<int:room_id>", views.rooms_delete),
    path("bookings/create", views.bookings_create),
    path("bookings/list", views.bookings_list),
    path("bookings/delete", views.booking_delete),
]
