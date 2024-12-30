from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Adjust 'home' to the name of your desired redirect view
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')  # Render the provided login HTML template


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            # Create the user
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to the login page
            
    return render(request, 'register.html')  # Render the provided register HTML template

def logout_view(request):

    auth_logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')

def home_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to log in to access the home page.')
        return redirect('login')
    return render(request, 'home.html')
