from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from apps.accounts.models import User
from .models import CollectionPoint, TrashBin


@transaction.atomic
def create_collection_point(*, creator, name, address, latitude, longitude, manager=None, trash_bins=None):
    if not creator.is_active or creator.suspended_at:
        raise PermissionDenied("Usuário suspenso não pode criar pontos de coleta.")

    if creator.role not in {User.Role.MANAGER, User.Role.ADMIN}:
        raise PermissionDenied("Apenas gestores ou administradores podem criar pontos de coleta.")

    if creator.role == User.Role.ADMIN and manager is not None:
        assigned_manager = manager
    else:
        assigned_manager = creator

    if assigned_manager.role not in {User.Role.MANAGER, User.Role.ADMIN}:
        raise ValidationError({"manager": "O responsável pelo ponto de coleta deve ser um gestor ou administrador."})

    point = CollectionPoint.objects.create(
        name=name,
        address=address,
        latitude=latitude,
        longitude=longitude,
        manager=assigned_manager,
    )

    if trash_bins:
        bins_to_create = []
        codes_seen = set()
        for item in trash_bins:
            code = (item.get("code") if isinstance(item, dict) else str(item)).strip()
            if not code:
                continue
            if code in codes_seen:
                raise ValidationError({"trashBins": f"O código de lixeira '{code}' foi informado mais de uma vez na requisição."})
            codes_seen.add(code)
            if TrashBin.objects.filter(code=code).exists():
                raise ValidationError({"trashBins": f"Já existe uma lixeira cadastrada com o código '{code}'."})
            bins_to_create.append(TrashBin(collection_point=point, code=code))

        if bins_to_create:
            TrashBin.objects.bulk_create(bins_to_create)

    return point


@transaction.atomic
def create_trash_bin(*, user, collection_point, code, occupancy_level=1, status=TrashBin.Status.AVAILABLE):
    if not user.is_active or user.suspended_at:
        raise PermissionDenied("Usuário suspenso não pode cadastrar lixeiras.")

    if user.role not in {User.Role.MANAGER, User.Role.ADMIN}:
        raise PermissionDenied("Apenas gestores ou administradores podem cadastrar lixeiras.")

    if user.role == User.Role.MANAGER and collection_point.manager != user:
        raise PermissionDenied("Gestores só podem cadastrar lixeiras em pontos de coleta sob sua responsabilidade.")

    code = str(code).strip()
    if not code:
        raise ValidationError({"code": "O código da lixeira é obrigatório."})

    if TrashBin.objects.filter(code=code).exists():
        raise ValidationError({"code": f"Já existe uma lixeira cadastrada com o código '{code}'."})

    if occupancy_level < 1 or occupancy_level > 4:
        raise ValidationError({"occupancyLevel": "O nível de ocupação deve estar entre 1 e 4."})

    if status not in TrashBin.Status.values:
        raise ValidationError({"status": "Status de lixeira inválido."})

    return TrashBin.objects.create(
        collection_point=collection_point,
        code=code,
        occupancy_level=occupancy_level,
        status=status,
    )


@transaction.atomic
def update_trash_bin(*, user, trash_bin, **kwargs):
    if not user.is_active or user.suspended_at:
        raise PermissionDenied("Usuário suspenso não pode alterar lixeiras.")

    if user.role not in {User.Role.MANAGER, User.Role.ADMIN}:
        raise PermissionDenied("Apenas gestores ou administradores podem alterar lixeiras.")

    if user.role == User.Role.MANAGER and trash_bin.collection_point.manager != user:
        raise PermissionDenied("Gestores só podem alterar lixeiras em pontos de coleta sob sua responsabilidade.")

    update_fields = ["updated_at"]

    if "code" in kwargs and kwargs["code"] is not None:
        new_code = str(kwargs["code"]).strip()
        if not new_code:
            raise ValidationError({"code": "O código da lixeira não pode ser vazio."})
        if TrashBin.objects.filter(code=new_code).exclude(pk=trash_bin.pk).exists():
            raise ValidationError({"code": f"Já existe uma lixeira cadastrada com o código '{new_code}'."})
        trash_bin.code = new_code
        update_fields.append("code")

    if "occupancy_level" in kwargs and kwargs["occupancy_level"] is not None:
        level = kwargs["occupancy_level"]
        if level < 1 or level > 4:
            raise ValidationError({"occupancyLevel": "O nível de ocupação deve estar entre 1 e 4."})
        trash_bin.occupancy_level = level
        update_fields.append("occupancy_level")
        if "status" not in kwargs and level > 3:
            trash_bin.status = TrashBin.Status.COLLECTION_REQUIRED
            update_fields.append("status")

    if "status" in kwargs and kwargs["status"] is not None:
        stat = kwargs["status"]
        if stat not in TrashBin.Status.values:
            raise ValidationError({"status": "Status de lixeira inválido."})
        trash_bin.status = stat
        if "status" not in update_fields:
            update_fields.append("status")

    if "collection_point" in kwargs and kwargs["collection_point"] is not None:
        new_point = kwargs["collection_point"]
        if user.role == User.Role.MANAGER and new_point.manager != user:
            raise PermissionDenied("Gestores não podem mover lixeiras para pontos de coleta que não gerenciam.")
        trash_bin.collection_point = new_point
        update_fields.append("collection_point")

    trash_bin.save(update_fields=update_fields)
    return trash_bin

