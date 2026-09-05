from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.collection_points.models import TrashBin
from apps.core.models import SoftDeleteModel


class WasteCategory(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Disposal(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="disposals")
    trash_bin = models.ForeignKey(TrashBin, on_delete=models.PROTECT, related_name="disposals")
    categories = models.ManyToManyField(WasteCategory, through="DisposalCategory")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    items_description = models.TextField()
    occupancy_level_reported = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    points_awarded = models.PositiveIntegerField(default=0)


class DisposalCategory(models.Model):
    disposal = models.ForeignKey(Disposal, on_delete=models.CASCADE)
    category = models.ForeignKey(WasteCategory, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("disposal", "category"), name="unique_disposal_category")]


class DisposalPhoto(models.Model):
    disposal = models.ForeignKey(Disposal, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="disposals/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)


class PointsTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="points_transactions")
    disposal = models.OneToOneField(Disposal, on_delete=models.PROTECT, related_name="points_transaction")
    points = models.PositiveIntegerField()
    reason = models.CharField(max_length=120, default="Registro de descarte")
    created_at = models.DateTimeField(auto_now_add=True)
