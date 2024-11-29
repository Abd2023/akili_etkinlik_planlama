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


def home_view(request):
    return render(request, 'home.html')


@login_required
def home(request):
    user = request.user

    # Kullanıcının katıldığı etkinlikler
    user_participated_event_ids = Participant.objects.filter(user=user).values_list('event_id', flat=True)

    # Önerilen etkinlikler
    user_interests = user.interests.split(", ") if user.interests else []
    recommended_events = Event.objects.filter(category__in=user_interests).exclude(id__in=user_participated_event_ids)

    # Genel etkinlikler (önerilen ve katıldığı etkinlikler hariç)
    general_events = Event.objects.exclude(id__in=recommended_events.values_list('id', flat=True)).exclude(id__in=user_participated_event_ids)

    # Kullanıcının katıldığı etkinlikler
    user_events = Event.objects.filter(id__in=user_participated_event_ids)

    # Şablona veriler gönderiliyor
    context = {
        'user': user,
        'recommended_events': recommended_events,
        'general_events': general_events,
        'user_events': user_events,
        'user_participated_event_ids': list(user_participated_event_ids),
    }
    return render(request, 'home.html', context)






# Function to check time conflicts
def check_time_conflicts(new_event):
    """
    Check if the new or updated event conflicts with existing events.
    """
    overlapping_events = Event.objects.filter(
        date=new_event.date,  # Same date
        start_time__lt=new_event.end_time,  # Overlaps with start time
        end_time__gt=new_event.start_time  # Overlaps with end time
    ).exclude(id=new_event.id)  # Exclude the event itself (useful for editing)
    return overlapping_events.exists()



@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user

            # Check for time conflicts
            if check_time_conflicts(event):
                form.add_error(None, "This event conflicts with an existing event.")
            else:
                event.save()

                # Award points for event creation
                request.user.total_points += 15
                request.user.save()

                return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'event_management/event_create.html', {'form': form})


def get_unread_message_count(user, event):
    return event.messages.exclude(read_by=user).count()

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

    if created:  # Eğer kullanıcı daha önce katılmamışsa
        request.user.total_points += 10  # Katılım puanı ekle
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
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)

            # Check for time conflicts
            if check_time_conflicts(updated_event):
                form.add_error(None, "This event conflicts with an existing event.")
            else:
                updated_event.save()
                return redirect('event_detail', event_id=updated_event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_management/event_edit.html', {'form': form, 'event': event})


def map_view(request):
    events = Event.objects.exclude(latitude=0.0, longitude=0.0).values("name", "latitude", "longitude", "location", "date", "start_time", "description")
    events_json = json.dumps(list(events), cls=DjangoJSONEncoder)  # Ensure this is JSON serializable
    return render(request, 'event_management/map_view.html', {
    'events': events_json,
    'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
})



def get_route(request):
    start = request.GET.get('start')
    end_lat = request.GET.get('end_lat')
    end_lng = request.GET.get('end_lng')
    mode = request.GET.get('mode', 'driving')  # Default to driving

    api_key = "5b3ce3597851110001cf6248b6e2696755f94c61bb3be94cc88b13d1"  # Replace with your API key
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



def event_map(request):
    events = Event.objects.values('name', 'latitude', 'longitude', 'location', 'date', 'start_time', 'description')
    
    print(list(events))  # Ensure this outputs the expected data
    events_serialized = json.dumps(list(events), cls=DjangoJSONEncoder) 
    return render(request, 'event_management/map.html', {'events': events_serialized})