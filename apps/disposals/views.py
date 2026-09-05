from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.models import User
from .models import Disposal, PointsTransaction, WasteCategory
from .serializers import DisposalCreateSerializer, DisposalSerializer, WasteCategorySerializer
from .services import create_disposal


class DisposalListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Disposal.objects.filter(user=self.request.user).select_related("trash_bin").prefetch_related("categories", "photos").order_by("-created_at")

    def get_serializer_class(self):
        return DisposalCreateSerializer if self.request.method == "POST" else DisposalSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        if hasattr(request.data, "getlist"):
            for key in request.data:
                if key == "categories":
                    data["categories"] = request.data.getlist("categories")
                else:
                    data[key] = request.data.get(key)
        elif isinstance(request.data, dict):
            data = request.data.copy()
        else:
            data = dict(request.data)

        photos = request.FILES.getlist("photos") or request.FILES.getlist("photo")
        if not photos and "photos" in request.data:
            photos_val = request.data.getlist("photos") if hasattr(request.data, "getlist") else request.data.get("photos")
            photos = photos_val if isinstance(photos_val, list) else [photos_val]
        data["photos"] = photos

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        values = serializer.validated_data
        disposal = create_disposal(
            user=request.user,
            trash_code=values["trashCode"],
            categories=values["categories"],
            quantity=values["quantity"],
            items_description=values["items_description"],
            occupancy_level_reported=values["occupancy_level_reported"],
            photos=values["photos"],
        )
        return Response(DisposalSerializer(disposal, context={"request": request}).data, status=201)


class DisposalDetailView(generics.RetrieveAPIView):
    serializer_class = DisposalSerializer

    def get_queryset(self):
        return Disposal.objects.filter(user=self.request.user).select_related("trash_bin").prefetch_related("categories", "photos")


class WasteCategoryListView(generics.ListAPIView):
    queryset = WasteCategory.objects.order_by("name")
    serializer_class = WasteCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RankingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.filter(is_active=True, role=User.Role.USER).annotate(points=Sum("points_transactions__points")).order_by("-points", "name")[:100]
        result = []
        for position, user in enumerate(users, 1):
            initials = "".join(part[0] for part in user.name.split()[:2]).upper()
            result.append({"id": user.id, "name": user.name, "points": user.points or 0, "position": position, "avatar": initials})
        return Response(result)
