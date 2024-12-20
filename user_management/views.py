from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from user_management.decorators import admin_required
from django.http import JsonResponse



from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import QueryDict

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        
        initial_data = QueryDict(request.META['QUERY_STRING'])
        form = CustomUserCreationForm(initial={
            'username': initial_data.get('username', ''),
            'email': initial_data.get('email', ''),
            'password1': initial_data.get('password', ''),
            'password2': initial_data.get('password', ''),
        })
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
   
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return render(request, 'user_management/profile.html')
    


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre!")
    return render(request, 'login_register.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Hesabınız başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz!")
            return redirect('login')
    return render(request, 'login_register.html')

def home_view(request):
    return render(request, 'home.html')




