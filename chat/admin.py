from django.contrib import admin
from .models import Message
from admin_panel.admin import custom_admin_site  # Use the custom admin site

@admin.register(Message, site=custom_admin_site)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('event', 'sender', 'timestamp', 'content')
    list_filter = ('event', 'sender', 'timestamp')
    search_fields = ('content', 'sender__username', 'event__name')
    ordering = ('-timestamp',)
    fields = ('event', 'sender', 'content', 'timestamp')
    readonly_fields = ('timestamp',)  # Ensure timestamp is not editable manually
