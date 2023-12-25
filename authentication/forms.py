from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User 
from django.conf import settings

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=settings.SIGN_UP_FIELDS

class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    