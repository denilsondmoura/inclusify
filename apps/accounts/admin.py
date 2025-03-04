from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    # Se você estiver usando email como login principal,
    # ajuste esses campos de acordo.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("nome_publico", "foto", "descricao_perfil")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
        ("Preferências", {"fields": ("theme", "font_size")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nome_publico", "password1", "password2", "theme", "font_size"),
        }),
    )
    list_display = ("email", "nome_publico", "is_staff")
    search_fields = ("email", "nome_publico")
    ordering = ("nome_publico",)
