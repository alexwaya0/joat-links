# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.online_status = True
            user.save()
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    user = request.user
    user.online_status = False
    user.save()
    logout(request)
    return redirect('login')


@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'core/profile_update.html', {'form': form})


@login_required
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return redirect('login')


@login_required
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('register')


@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    matches = CustomUser.objects.filter(
        gender=user.preferred_gender,
        is_active=True,
        location=user.location,
    ).exclude(id=user.id)
    return render(request, 'core/dashboard.html', {'matches': matches})

