from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class GreenUpUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "name", "role", "is_active")
    fieldsets = ((None, {"fields": ("email", "password")}), ("Perfil", {"fields": ("name", "phone", "cpf", "role", "suspended_at")}), ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}))
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "name", "password1", "password2", "role")}),)
