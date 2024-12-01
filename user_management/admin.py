from django.contrib import admin
from .models import CustomUser  
from admin_panel.admin import custom_admin_site 

@admin.register(CustomUser, site=custom_admin_site) 
class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'email', 'role', 'total_points', 'first_participation_bonus_awarded')
    list_filter = ('role', 'first_participation_bonus_awarded', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-total_points', 'username')  

    
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

    
    readonly_fields = ('total_points',)

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 
                       'is_staff', 'is_active'),
        }),
    )
