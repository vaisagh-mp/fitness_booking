from django.db import models
from django.utils import timezone

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # On create (no ID yet), set available_slots = total_slots
        if self._state.adding and self.available_slots is None:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} by {self.instructor} at {self.date_time}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name="bookings")
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

