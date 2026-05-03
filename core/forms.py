from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)