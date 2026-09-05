from django.urls import path
from .views import (
    CollectionPointDetailView,
    CollectionPointListCreateView,
    CollectionPointTrashBinListCreateView,
    TrashBinByCodeView,
    TrashBinDetailUpdateView,
    TrashBinListCreateView,
)

urlpatterns = [
    path("", CollectionPointListCreateView.as_view(), name="collection_points"),
    path("<int:pk>/", CollectionPointDetailView.as_view(), name="collection_point"),
    path("<int:point_pk>/trash-bins/", CollectionPointTrashBinListCreateView.as_view(), name="collection_point_trash_bins"),
    path("trash-bins/", TrashBinListCreateView.as_view(), name="trash_bins"),
    path("trash-bins/<int:pk>/", TrashBinDetailUpdateView.as_view(), name="trash_bin_detail"),
    path("trash-bins/by-code/<str:code>/", TrashBinByCodeView.as_view(), name="trash_bin_by_code"),
]

