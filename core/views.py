# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import CustomUser, ChatMessage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_GET

from datetime import timedelta


# from .models import UserProfile  # Assuming you have a UserProfile model with preferred gender field



def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = True  # Modify as needed for future verification logic
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    user = request.user
    if query:
        results = CustomUser.objects.filter(
            Q(username__icontains=query) | Q(location__icontains=query),
            gender=user.preferred_gender,
            is_active=True,
            online_status=True
        ).exclude(id=user.id)
    else:
        results = CustomUser.objects.filter(
            gender=user.preferred_gender,
            is_active=True,
            online_status=True
        ).exclude(id=user.id)
    return render(request, 'core/search_results.html', {'results': results, 'query': query})

@require_GET
@login_required
def live_online_users(request):
    # Get the logged-in user's preferred gender
    preferred_gender = request.user.profile.preferred_gender
    
    # Get all users online (filtered by preferred gender)
    # Assuming we have a method `is_online` that checks if a user is online
    online_users = UserProfile.objects.filter(gender=preferred_gender, is_online=True)
    
    users_data = []
    for user in online_users:
        users_data.append({
            'username': user.user.username,
            'profile_picture': user.profile_picture.url if user.profile_picture else '',
            'age': user.age,
            'gender': user.gender,
            'location': user.location,
        })

    return JsonResponse({'users': users_data})

@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'core/profile_update.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user.online_status = True
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
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

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Check for recent identical message
            recent_time = timezone.now() - timedelta(seconds=30)
            exists = ChatMessage.objects.filter(
                sender=request.user,
                receiver=other_user,
                message=message,
                timestamp__gte=recent_time
            ).exists()

            if not exists:
                ChatMessage.objects.create(sender=request.user, receiver=other_user, message=message)

    messages = ChatMessage.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, 'core/chat.html', {'messages': messages, 'other_user': other_user})