from django.db import models

class Room(models.Model):
    description = models.TextField()
    price_per_night = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Room #{self.id}"
    

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["room", "date_start"])]

    def __str__(self) -> str:
        return f"Booking #{self.id} (room {self.room_id})"

