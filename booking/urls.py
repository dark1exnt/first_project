from django.urls import path

from booking import views

urlpatterns = [
    path("rooms/create", views.rooms_create),
    path("rooms/list", views.rooms_list),
    path("rooms/delete", views.rooms_delete),
    path("bookings/create", views.bookings_create),
    path("bookings/list", views.bookings_list),
]
