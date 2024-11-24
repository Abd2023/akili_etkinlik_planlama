from django.contrib import admin
from .models import UserInterest, EventCategory, EventConflict

admin.site.register(UserInterest)
admin.site.register(EventCategory)
admin.site.register(EventConflict)