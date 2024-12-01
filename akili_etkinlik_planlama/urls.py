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
from event_management.views import home 
from event_management.admin_views import admin_report  
from admin_panel.admin import custom_admin_site  
from user_management.views import login
from django.conf import settings
from django.conf.urls.static import static  
from django.views.generic import TemplateView  
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    path('admin/', include('admin_panel.urls')),
    #path('admin/', custom_admin_site.urls), 
    path('user/', include('user_management.urls')), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
    path('events/', include('event_management.urls')),  
    path('home/', home, name='home'),  
    path('events/', include('event_management.urls')),
    path('chat/', include('chat.urls', namespace='chat')),  
    path('admin/reports/', admin_report, name='admin_report'),  
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)