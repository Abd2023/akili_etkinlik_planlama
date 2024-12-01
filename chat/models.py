from django.db import models
from django.conf import settings
from event_management.models import Event

class Message(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="read_messages", blank=True) 

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.name}"
