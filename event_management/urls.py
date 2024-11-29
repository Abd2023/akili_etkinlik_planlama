# event_management/urls.py
from django.urls import path
from . import views
from .views import home_view


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),  # For event detail
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),  # For event edit
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/join/', views.join_event, name='join_event'),
    path('<int:event_id>/leave/', views.leave_event, name='leave_event'),
    path('home/', home_view, name='home'),
    #path('map/', views.map_view, name='map_view'), 
    path('map/', views.event_map, name='event_map'),
    path('<int:event_id>/join/', views.join_event, name='join_event'),
     path('events/', views.event_list, name='event_list'),  # Event list
]
