from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Adicionando o email como campo obrigatório

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]