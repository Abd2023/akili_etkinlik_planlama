from django.contrib import admin
from .models import CustomUser  # Import your CustomUser model

admin.site.register(CustomUser)  # Register the model with the admin site
