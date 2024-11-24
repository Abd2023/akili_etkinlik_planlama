from django.db import models
from django.conf import settings
from event_management.models import Event

class UserInterest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_interests")
    interest = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.interest}"


class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="categories")
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.event.name} - {self.category}"

class EventConflict(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="conflicts")
    conflicting_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="conflicting_with")
    conflict_reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event.name} conflicts with {self.conflicting_event.name}"
