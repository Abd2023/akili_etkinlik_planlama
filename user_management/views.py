from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from user_management.decorators import admin_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_management/register.html', {'form': form})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'user_management/profile_update.html', {'form': form})

@admin_required
def admin_dashboard(request):
    return render(request, 'user_management/admin_dashboard.html')

@login_required
def profile(request):
    # Check if the user is an admin
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return render(request, 'user_management/profile.html')
