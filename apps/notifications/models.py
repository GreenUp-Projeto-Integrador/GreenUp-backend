from django.conf import settings
from django.db import models
from apps.collection_points.models import TrashBin
from apps.core.models import SoftDeleteModel


class Notification(SoftDeleteModel):
    class Type(models.TextChoices):
        COLLECTION_REQUIRED = "COLLECTION_REQUIRED", "Coleta necessária"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notifications")
    trash_bin = models.ForeignKey(TrashBin, on_delete=models.PROTECT, related_name="notifications")
    notification_type = models.CharField(max_length=30, choices=Type.choices)
    message = models.CharField(max_length=255)
    read_at = models.DateTimeField(null=True, blank=True)
