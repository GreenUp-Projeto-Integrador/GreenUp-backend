from django.contrib import admin
from .models import Disposal, DisposalCategory, DisposalPhoto, PointsTransaction, WasteCategory

admin.site.register([Disposal, DisposalCategory, DisposalPhoto, PointsTransaction, WasteCategory])
