from django.shortcuts import render
from .forms import EventForm
from .models import Event
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import  Participant

from django.core.exceptions import ValidationError

import requests
from django.http import JsonResponse


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required
def home(request):
    user = request.user

    
    user_participated_event_ids = Participant.objects.filter(user=user).values_list('event_id', flat=True)

   
    user_interests = user.interests.split(", ") if user.interests else []
    recommended_events = Event.objects.filter(category__in=user_interests).exclude(id__in=user_participated_event_ids)

    
    general_events = Event.objects.exclude(id__in=recommended_events.values_list('id', flat=True)).exclude(id__in=user_participated_event_ids)

    
    user_events = Event.objects.filter(id__in=user_participated_event_ids)

    
    context = {
        'user': user,
        'recommended_events': recommended_events,
        'general_events': general_events,
        'user_events': user_events,
        'user_participated_event_ids': list(user_participated_event_ids),
    }
    return render(request, 'home.html', context)







def check_time_conflicts(new_event):
    """
    Check if the new or updated event conflicts with existing events.
    """
    overlapping_events = Event.objects.filter(
        date=new_event.date,  
        start_time__lt=new_event.end_time,  
        end_time__gt=new_event.start_time  
    ).exclude(id=new_event.id)  
    return overlapping_events.exists()



@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            if check_time_conflicts(event):
                form.add_error(None, "This event conflicts with an existing event.")
            else:
                event.save()
                request.user.total_points += 15
                request.user.save()
                return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_management/event_create.html', {'form': form})



def get_unread_message_count(user, event):
    return event.messages.exclude(read_by=user).count()


@login_required
def event_list(request):
    events = Event.objects.all()
    events_with_participation = []
    
    for event in events:
        is_participant = Participant.objects.filter(user=request.user, event=event).exists()
        unread_count = get_unread_message_count(request.user, event)
        events_with_participation.append((event, is_participant, unread_count))
    
    return render(request, 'event_management/event_list.html', {
        'events_with_participation': events_with_participation,
    })


@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participant, created = Participant.objects.get_or_create(user=request.user, event=event)

    if created:  
        request.user.total_points += 10  
        request.user.save()

    return redirect('/home/')


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Participant.objects.filter(user=request.user, event=event).delete()
    return redirect('/home/')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_management/event_detail.html', {'event': event})


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)  
        if form.is_valid():
            updated_event = form.save(commit=False)
            if check_time_conflicts(updated_event):
                form.add_error(None, "This event conflicts with an existing event.")
            else:
                updated_event.save()
                return redirect('event_detail', event_id=updated_event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_management/event_edit.html', {'form': form, 'event': event})







def get_route(request):
    start = request.GET.get('start')
    end_lat = request.GET.get('end_lat')
    end_lng = request.GET.get('end_lng')
    mode = request.GET.get('mode', 'driving')  

    api_key = "5b3ce3597851110001cf6248b6e2696755f94c61bb3be94cc88b13d1"  
    url = f"https://api.openrouteservice.org/v2/directions/{mode}"
    headers = {"Authorization": api_key}
    params = {
        "start": start,
        "end": f"{end_lng},{end_lat}",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Unable to fetch route"}, status=500)


@login_required
def event_map(request):
    events = Event.objects.values('name', 'latitude', 'longitude', 'location', 'date', 'start_time', 'description')
    
    
    events_serialized = json.dumps(list(events), cls=DjangoJSONEncoder) 
    return render(request, 'event_management/map.html', {'events': events_serialized})