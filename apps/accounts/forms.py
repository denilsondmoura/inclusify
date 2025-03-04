from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Adicionando o email como campo obrigatório

    class Meta:
        model = Profile
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]