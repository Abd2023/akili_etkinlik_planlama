from django.contrib import admin
from .models import CustomUser  # Import your CustomUser model
from admin_panel.admin import custom_admin_site  # Use the custom admin site

@admin.register(CustomUser, site=custom_admin_site)  # Register with the custom admin site
class CustomUserAdmin(admin.ModelAdmin):
    # Display the main user details in the admin list view
    list_display = ('username', 'email', 'role', 'total_points', 'first_participation_bonus_awarded')
    list_filter = ('role', 'first_participation_bonus_awarded', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-total_points', 'username')  # Default ordering by total points

    # Configure fieldsets for better organization in the admin detail view
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 
                       'phone_number', 'location', 'interests', 'profile_picture')
        }),
        ('Points and Achievements', {
            'fields': ('total_points', 'first_participation_bonus_awarded')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Role Management', {
            'fields': ('role',)
        }),
    )

    # Add read-only fields to prevent manual editing of auto-calculated fields
    readonly_fields = ('total_points',)

    # Customize the add form for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 
                       'is_staff', 'is_active'),
        }),
    )
