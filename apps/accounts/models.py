from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("user", "Usuário"),
    ("admin", "Administrador"),
)
THEME_CHOICES = (
    ("light", "Claro"),
    ("dark", "Escuro"),
)
class Profile(AbstractUser):
    # Substitui o campo username pelo email como identificador principal (opcional)
    # Se quiser usar o email como principal login:
    # username = None
    # email = models.EmailField("email address", unique=True)s

    nome_publico = models.CharField(max_length=150, blank=False, null=False)
    foto = models.ImageField(upload_to="fotos_perfil/", blank=True, null=True)
    descricao_perfil = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="light")
    font_size = models.IntegerField(default=14)

    # Caso você deseje usar o email como campo principal de login,
    # descomente as linhas abaixo e comente o username:
    #
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []  # Campos obrigatórios além do email para criar superuser

    def __str__(self):
        return self.nome_publico