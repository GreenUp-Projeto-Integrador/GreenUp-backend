from rest_framework import serializers
from apps.accounts.models import User
from .models import CollectionPoint, TrashBin


class TrashBinSerializer(serializers.ModelSerializer):
    occupancyLevel = serializers.IntegerField(source="occupancy_level", read_only=True)
    collectionPointId = serializers.IntegerField(source="collection_point_id", read_only=True)

    class Meta:
        model = TrashBin
        fields = ("id", "code", "occupancyLevel", "status", "collectionPointId")


class TrashBinCreateSerializer(serializers.ModelSerializer):
    collectionPointId = serializers.PrimaryKeyRelatedField(
        source="collection_point",
        queryset=CollectionPoint.objects.filter(is_active=True),
        required=False,
    )
    occupancyLevel = serializers.IntegerField(
        source="occupancy_level", min_value=1, max_value=4, default=1, required=False
    )

    class Meta:
        model = TrashBin
        fields = ("id", "code", "occupancyLevel", "status", "collectionPointId")


class TrashBinUpdateSerializer(serializers.ModelSerializer):
    collectionPointId = serializers.PrimaryKeyRelatedField(
        source="collection_point",
        queryset=CollectionPoint.objects.filter(is_active=True),
        required=False,
    )
    occupancyLevel = serializers.IntegerField(
        source="occupancy_level", min_value=1, max_value=4, required=False
    )
    code = serializers.CharField(max_length=30, required=False)
    status = serializers.ChoiceField(choices=TrashBin.Status.choices, required=False)

    class Meta:
        model = TrashBin
        fields = ("id", "code", "occupancyLevel", "status", "collectionPointId")



class CollectionPointSerializer(serializers.ModelSerializer):
    trashBins = TrashBinSerializer(source="trash_bins", many=True, read_only=True)

    class Meta:
        model = CollectionPoint
        fields = ("id", "name", "address", "latitude", "longitude", "trashBins")


class CollectionPointCreateSerializer(serializers.ModelSerializer):
    managerId = serializers.PrimaryKeyRelatedField(
        source="manager",
        queryset=User.objects.filter(is_active=True, role__in=[User.Role.MANAGER, User.Role.ADMIN]),
        required=False,
        allow_null=True,
    )
    trashBins = serializers.ListField(
        child=serializers.CharField(max_length=30),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = CollectionPoint
        fields = ("id", "name", "address", "latitude", "longitude", "managerId", "trashBins")

    def to_internal_value(self, data):
        if "trashBins" in data and isinstance(data["trashBins"], list):
            data = data.copy()
            cleaned = []
            for item in data["trashBins"]:
                if isinstance(item, dict) and "code" in item:
                    cleaned.append(item["code"])
                elif isinstance(item, str):
                    cleaned.append(item)
                else:
                    cleaned.append(item)
            data["trashBins"] = cleaned
        return super().to_internal_value(data)

