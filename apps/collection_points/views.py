from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.accounts.permissions import IsManagerOrAdmin
from .models import CollectionPoint, TrashBin
from .serializers import (
    CollectionPointCreateSerializer,
    CollectionPointSerializer,
    TrashBinCreateSerializer,
    TrashBinSerializer,
    TrashBinUpdateSerializer,
)
from .services import create_collection_point, create_trash_bin, update_trash_bin


class CollectionPointListCreateView(generics.ListCreateAPIView):
    queryset = CollectionPoint.objects.select_related("manager").prefetch_related("trash_bins")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManagerOrAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CollectionPointCreateSerializer
        return CollectionPointSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        point = create_collection_point(
            creator=request.user,
            name=values["name"],
            address=values["address"],
            latitude=values["latitude"],
            longitude=values["longitude"],
            manager=values.get("manager"),
            trash_bins=values.get("trashBins"),
        )
        return Response(CollectionPointSerializer(point, context={"request": request}).data, status=status.HTTP_201_CREATED)


CollectionPointListView = CollectionPointListCreateView


class CollectionPointDetailView(generics.RetrieveAPIView):
    queryset = CollectionPoint.objects.prefetch_related("trash_bins")
    serializer_class = CollectionPointSerializer
    permission_classes = [AllowAny]


class CollectionPointTrashBinListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManagerOrAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TrashBinCreateSerializer
        return TrashBinSerializer

    def get_queryset(self):
        point = generics.get_object_or_404(CollectionPoint.objects.filter(is_active=True), pk=self.kwargs["point_pk"])
        return TrashBin.objects.filter(collection_point=point, is_active=True).select_related("collection_point").order_by("code")

    def create(self, request, *args, **kwargs):
        point = generics.get_object_or_404(CollectionPoint.objects.filter(is_active=True), pk=self.kwargs["point_pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        trash_bin = create_trash_bin(
            user=request.user,
            collection_point=point,
            code=values["code"],
            occupancy_level=values.get("occupancy_level", 1),
            status=values.get("status", TrashBin.Status.AVAILABLE),
        )
        return Response(TrashBinSerializer(trash_bin, context={"request": request}).data, status=status.HTTP_201_CREATED)


class TrashBinListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TrashBinCreateSerializer
        return TrashBinSerializer

    def get_queryset(self):
        queryset = TrashBin.objects.filter(is_active=True).select_related("collection_point").order_by("id")
        point_id = self.request.query_params.get("collection_point")
        if point_id:
            queryset = queryset.filter(collection_point_id=point_id)
        stat = self.request.query_params.get("status")
        if stat:
            queryset = queryset.filter(status=stat)
        return queryset


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        point = values.get("collection_point")
        if not point:
            raise ValidationError({"collectionPointId": "O ponto de coleta é obrigatório."})
        trash_bin = create_trash_bin(
            user=request.user,
            collection_point=point,
            code=values["code"],
            occupancy_level=values.get("occupancy_level", 1),
            status=values.get("status", TrashBin.Status.AVAILABLE),
        )
        return Response(TrashBinSerializer(trash_bin, context={"request": request}).data, status=status.HTTP_201_CREATED)


class TrashBinDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TrashBin.objects.filter(is_active=True).select_related("collection_point")

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TrashBinUpdateSerializer
        return TrashBinSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        trash_bin = update_trash_bin(
            user=request.user,
            trash_bin=instance,
            **values,
        )
        return Response(TrashBinSerializer(trash_bin, context={"request": request}).data)


class TrashBinByCodeView(generics.RetrieveAPIView):
    queryset = TrashBin.objects.select_related("collection_point")
    serializer_class = TrashBinSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "code"

