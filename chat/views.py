from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from event_management.models import Event, Participant
from .models import Message
import json

from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

from django.db.models import Count

# Create your views here.
#


@login_required
@require_POST
def send_message(request):
    """
    Save a message from the user into the database.
    Validate that the user is a participant of the event before sending the message.
    """
    try:
        
        data = json.loads(request.body)
        event_id = data.get("event_id")
        content = data.get("content")

        if not event_id or not content:
            return JsonResponse({"error": "Event ID and message content are required."}, status=400)

        
        event = get_object_or_404(Event, id=event_id)

        
        is_participant = Participant.objects.filter(event=event, user=request.user).exists()
        if not is_participant:
            return JsonResponse({"error": "You are not a participant of this event."}, status=403)

        
        message = Message.objects.create(event=event, sender=request.user, content=content)
        return JsonResponse({"success": True, "message_id": message.id, "timestamp": message.timestamp}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    

@require_GET
def get_messages(request, event_id):
    """
    Fetch all messages for a given event.
    Paginate messages if the event has a large number of messages.
    """
    try:
        
        event = get_object_or_404(Event, id=event_id)

       
        messages = Message.objects.filter(event=event).order_by("-timestamp")

        
        paginator = Paginator(messages, 20)  
        page_number = request.GET.get("page", 1)
        page = paginator.get_page(page_number)

        
        message_data = [
            {
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in page
        ]

        return JsonResponse({
            "messages": message_data,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
            "total_pages": paginator.num_pages,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@login_required
def messaging_panel(request, event_id):
    event = get_object_or_404(Event, id=event_id)

   
    unread_messages = event.messages.exclude(read_by=request.user)
    for message in unread_messages:
        message.read_by.add(request.user)

    messages = event.messages.order_by('timestamp')  
    return render(request, 'chat/messaging_panel.html', {'event': event, 'messages': messages})


def get_total_unread_message_count(user):
    return Message.objects.exclude(read_by=user).filter(event__participants=user).count()

def dashboard(request):
    total_unread_messages = get_total_unread_message_count(request.user)
    return render(request, 'dashboard.html', {'total_unread_messages': total_unread_messages})
