from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from apps.collection_points.models import TrashBin
from apps.notifications.models import Notification
from .models import Disposal, DisposalCategory, DisposalPhoto, PointsTransaction

POINTS_PER_ITEM = 10


@transaction.atomic
def create_disposal(*, user, trash_code, categories, quantity, items_description, occupancy_level_reported, photos):
    if not user.is_active or user.suspended_at:
        raise PermissionDenied("Usuário suspenso não pode registrar descartes.")
    try:
        trash_bin = TrashBin.objects.select_for_update().select_related("collection_point__manager").get(code=trash_code)
    except TrashBin.DoesNotExist as exc:
        raise ValidationError({"trashCode": "Lixeira ativa não encontrada."}) from exc

    previous_level = trash_bin.occupancy_level
    points = quantity * POINTS_PER_ITEM
    disposal = Disposal.objects.create(
        user=user,
        trash_bin=trash_bin,
        quantity=quantity,
        items_description=items_description,
        occupancy_level_reported=occupancy_level_reported,
        points_awarded=points,
    )
    DisposalCategory.objects.bulk_create([DisposalCategory(disposal=disposal, category=category) for category in categories])
    for photo in photos:
        DisposalPhoto.objects.create(disposal=disposal, image=photo)
    PointsTransaction.objects.create(user=user, disposal=disposal, points=points)

    trash_bin.occupancy_level = occupancy_level_reported
    if occupancy_level_reported > 3:
        trash_bin.status = TrashBin.Status.COLLECTION_REQUIRED
    trash_bin.save(update_fields=["occupancy_level", "status", "updated_at"])

    if previous_level <= 3 < occupancy_level_reported:
        Notification.objects.create(
            recipient=trash_bin.collection_point.manager,
            trash_bin=trash_bin,
            notification_type=Notification.Type.COLLECTION_REQUIRED,
            message=f"A lixeira {trash_bin.code} atingiu o nível 4 e precisa de coleta.",
        )
    return disposal
