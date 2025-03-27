from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    
    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'foto', 'descricao_perfil',
            'password1', 'password2'
        ]
        labels = {
            'username': 'Nome de Usuário',
            'foto': 'Foto de Perfil',
            'descricao_perfil': 'Descrição do Perfil'
        }
        help_texts = {
            'username': None,  # Remove o help text padrão
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes Bootstrap aos campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})