import uuid

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True, blank=True, default=None)
    location = models.CharField(max_length=100, null=True, blank=True, default="Online")
    image = models.ImageField(upload_to="event_images", blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    code = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)