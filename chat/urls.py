from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    
    path("event/<int:event_id>/", views.messaging_panel, name="messaging_panel"),
    path('send/', views.send_message, name='send_message'),
    path('messages/<int:event_id>/', views.get_messages, name='get_messages'),
]
