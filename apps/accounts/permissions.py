from rest_framework.permissions import BasePermission
from .models import User


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_active and request.user.role in {User.Role.MANAGER, User.Role.ADMIN})


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_active and request.user.role == User.Role.ADMIN)
