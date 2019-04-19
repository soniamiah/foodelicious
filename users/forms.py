from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.conf import settings
import requests

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #default required= true

    class Meta: #nested configuration in one place. model effected is usermodel fields in order:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    class Meta: #nested configuration in one place. model effected is usermodel fields in order:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ['image']
