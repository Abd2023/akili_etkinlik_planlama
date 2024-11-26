from django.contrib import admin
from .models import CustomUser  # Import your CustomUser model


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'total_points', 'first_participation_bonus_awarded')
    list_filter = ('first_participation_bonus_awarded',)
