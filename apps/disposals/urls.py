from django.urls import path
from .views import DisposalDetailView, DisposalListCreateView, WasteCategoryListView

urlpatterns = [
    path("", DisposalListCreateView.as_view(), name="disposals"),
    path("categories/", WasteCategoryListView.as_view(), name="waste_categories"),
    path("<int:pk>/", DisposalDetailView.as_view(), name="disposal_detail"),
]
