from django import forms
from .models import Postagem
from django_summernote.widgets import SummernoteWidget
from django.forms.widgets import TextInput, SelectMultiple

class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'corpo', 'topicos']
        widgets = {
            'titulo': TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'corpo': SummernoteWidget(),  # Usando Summernote aqui
            'topicos': SelectMultiple(attrs={'class': 'form-select'}),
        }
    