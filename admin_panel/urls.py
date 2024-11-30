from django.urls import path
from . import views
from admin_panel.views import admin_update_user

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('manage-events/', views.manage_events, name='admin_manage_events'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('admin/update-user/<int:user_id>/', admin_update_user, name='admin_update_user'),
    path('manage-users/', views.manage_users, name='manage_users'),
]
