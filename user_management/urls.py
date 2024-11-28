from django.urls import path
from . import views
from .views import login_view, register_view, home_view
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/', views.profile, name='profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
]
