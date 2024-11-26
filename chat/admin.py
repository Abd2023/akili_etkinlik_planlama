from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("event", "sender", "timestamp", "content")
    list_filter = ("event", "timestamp")
    search_fields = ("sender__username", "content")


