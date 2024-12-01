from django.contrib.admin import AdminSite
from django.urls import path
from event_management.admin_views import admin_report  

class CustomAdminSite(AdminSite):
    site_header = "Event Management Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to the Admin Panel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reports/', admin_report, name='admin_report'), 
        ]
        return custom_urls + urls


custom_admin_site = CustomAdminSite(name='custom_admin')
