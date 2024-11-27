"""
URL configuration for akili_etkinlik_planlama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from event_management.views import home  # Import the home view
from event_management.admin_views import admin_report  # Import your view
from admin_panel.admin import custom_admin_site  # Import your custom admin site  # Import the custom admin site



urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Use the custom admin site
    path('user/', include('user_management.urls')),  # This includes user_management URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Use Django's default login template
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add logout URL
    path('events/', include('event_management.urls')),  # Include event_management URLs under /events/
    path('home/', home, name='home'),  # Add the home view
    path('events/', include('event_management.urls')),
    path('chat/', include('chat.urls', namespace='chat')),  # Add this line
    path('admin/reports/', admin_report, name='admin_report'),  # Add admin reports

]
