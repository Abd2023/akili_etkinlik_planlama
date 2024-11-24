from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/', views.profile, name='profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
