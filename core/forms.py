# core/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border p-2 rounded w-full'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'border p-2 rounded w-full'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
