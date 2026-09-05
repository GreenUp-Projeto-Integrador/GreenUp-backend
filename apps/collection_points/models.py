from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.core.models import SoftDeleteModel


class CollectionPoint(SoftDeleteModel):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="managed_collection_points")

    def __str__(self):
        return self.name


class TrashBin(SoftDeleteModel):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponível"
        COLLECTION_REQUIRED = "COLLECTION_REQUIRED", "Coleta necessária"
        MAINTENANCE = "MAINTENANCE", "Manutenção"

    collection_point = models.ForeignKey(CollectionPoint, on_delete=models.PROTECT, related_name="trash_bins")
    code = models.CharField(max_length=30, unique=True)
    occupancy_level = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return self.code
