from django.shortcuts import render
from .forms import EventForm
from .models import Event


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import  Participant

from django.core.exceptions import ValidationError



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
                return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_management/event_create.html', {'form': form})


def event_list(request):
    events = Event.objects.all()
    events_with_participation = []
    
    for event in events:
        is_participant = Participant.objects.filter(user=request.user, event=event).exists()
        events_with_participation.append((event, is_participant))
    
    return render(request, 'event_management/event_list.html', {
        'events_with_participation': events_with_participation,
    })



@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Participant.objects.get_or_create(user=request.user, event=event)
    return redirect('event_list')

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Participant.objects.filter(user=request.user, event=event).delete()
    return redirect('event_list')


# Event detail view
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