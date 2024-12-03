from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField(default="12:00:00", blank=True, null=True)
    end_time = models.TimeField(default="12:00:00", blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  
   

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Custom validation to check for time conflicts."""
        if self.start_time >= self.end_time:
            raise ValidationError(_("Start time must be before end time."))

        overlapping_events = Event.objects.filter(
            date=self.date,
            location=self.location,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id) 

        if overlapping_events.exists():
            raise ValidationError(
                _("This event conflicts with another event in the same location.")
            )

    def save(self, *args, **kwargs):
       
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
