from django.contrib import admin
from admin_panel.admin import custom_admin_site  # Import your custom admin site
from .models import Event, Participant


@admin.register(Event, site=custom_admin_site)  # Register Event with the custom admin site
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'created_by')
    list_filter = ('date', 'category', 'created_by')
    search_fields = ('name', 'description', 'location')
    ordering = ('-date',)
    fields = ('name', 'description', 'location', 'date', 'start_time', 'end_time', 'created_by', 'latitude', 'longitude', 'category')
    readonly_fields = ('created_by',)  # Example of making some fields read-only


@admin.register(Participant, site=custom_admin_site)  # Register Participant with the custom admin site
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'joined_at')
    list_filter = ('event', 'joined_at')
    search_fields = ('user__username', 'event__name')
    ordering = ('-joined_at',)
