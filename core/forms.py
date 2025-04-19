# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'whatsapp_number', 'date_of_birth',
            'profile_picture', 'gender', 'location', 'preferred_gender', 'password1', 'password2'
        ]

class LoginForm(AuthenticationForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = [
            'email', 'whatsapp_number', 'date_of_birth', 'profile_picture', 'gender', 'location', 'preferred_gender'
        ]

