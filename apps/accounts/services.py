from django.utils import timezone
from rest_framework.exceptions import ValidationError


def change_password(user, current_password, new_password):
    if not user.check_password(current_password):
        raise ValidationError({"currentPassword": "A senha atual está incorreta."})
    user.set_password(new_password)
    user.save(update_fields=["password"])


def suspend_user(user):
    if user.role == user.Role.ADMIN:
        raise ValidationError("Contas administrativas não podem ser suspensas por esta operação.")
    user.is_active = False
    user.suspended_at = timezone.now()
    user.save(update_fields=["is_active", "suspended_at"])


def reactivate_user(user):
    user.is_active = True
    user.suspended_at = None
    user.save(update_fields=["is_active", "suspended_at"])
