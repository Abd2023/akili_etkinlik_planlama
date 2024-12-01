from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from user_management.models import CustomUser
from event_management.models import Event
from django.db.models import Count
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

from user_management.forms import ProfileUpdateForm
from django.contrib.auth.models import User

def is_superuser(user):
    return user.is_superuser



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser: 
            login(request, user)
            return redirect('admin_dashboard')  
        else:
            messages.error(request, "Sadece admin kullanıcıları giriş yapabilir!")
            return redirect('admin_login')  

    return render(request, 'admin/admin_login.html') 


@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    
    total_users = CustomUser.objects.count()
    total_events = Event.objects.count()

    
    users = CustomUser.objects.annotate(event_count=Count('event'))
    events = Event.objects.all()  

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'events': events,
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_superuser)
def manage_users(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'admin/manage_users.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, "Kullanıcı başarıyla silindi.")
    return redirect('manage_users')  


@login_required
@user_passes_test(is_superuser)
def manage_events(request):
    events = Event.objects.all()
    return render(request, 'admin/manage_events.html', {'events': events})


@login_required
@user_passes_test(is_superuser)
def manage_events(request):
    events = Event.objects.all()
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        action = request.POST.get('action')
        event = get_object_or_404(Event, id=event_id)
        if action == "activate":
            event.is_active = True
        elif action == "deactivate":
            event.is_active = False
        event.save()
        messages.success(request, "Event status updated successfully.")
    context = {'events': events}
    return render(request, 'admin/manage_events.html', context)



def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'admin/event_details.html', {'event': event})


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.date = request.POST.get('date')
        event.location = request.POST.get('location')
        event.save()
        return redirect('admin_dashboard')
    return render(request, 'admin/edit_event.html', {'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('admin_dashboard')


User = get_user_model()  

def admin_update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'admin/admin_profile_update.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def manage_users(request):
    users = CustomUser.objects.all()  
    user_event_data = []

    for user in users:
        
        events = Event.objects.filter(participants__user=user)
        user_event_data.append({
            'user': user,
            'events': events
        })

    context = {
        'user_event_data': user_event_data,
    }
    return render(request, 'admin/manage_users.html', context)

@login_required
@user_passes_test(is_superuser)
def toggle_admin_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_superuser:
        user.is_superuser = False
        messages.success(request, f"{user.username} artık admin değil.")
    else:
        user.is_superuser = True
        messages.success(request, f"{user.username} artık admin.")
    user.save()
    return redirect('manage_users')

