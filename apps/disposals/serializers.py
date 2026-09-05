import json
from rest_framework import serializers
from .models import Disposal, DisposalPhoto, WasteCategory


class DisposalPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisposalPhoto
        fields = ("id", "image")


class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ("id", "name")


class DisposalCreateSerializer(serializers.Serializer):
    trashCode = serializers.CharField(max_length=30)
    categories = serializers.PrimaryKeyRelatedField(queryset=WasteCategory.objects.all(), many=True, allow_empty=False)
    quantity = serializers.IntegerField(min_value=1)
    items = serializers.CharField(source="items_description", allow_blank=False)
    trashLevel = serializers.IntegerField(source="occupancy_level_reported", min_value=1, max_value=4)
    photos = serializers.ListField(child=serializers.ImageField(), allow_empty=False, write_only=True)

    def to_internal_value(self, data):
        # Convert QueryDict or dict-like data to a mutable dictionary
        if hasattr(data, "dict") and hasattr(data, "getlist"):
            converted = {}
            for key in data:
                if key == "categories":
                    converted[key] = data.getlist("categories")
                elif key in ("photos", "photo"):
                    converted["photos"] = data.getlist(key)
                else:
                    converted[key] = data.get(key)
        elif isinstance(data, dict):
            converted = data.copy()
        else:
            converted = dict(data)

        # Convert numeric string to int for quantity
        if "quantity" in converted and converted["quantity"] is not None:
            try:
                converted["quantity"] = int(str(converted["quantity"]).strip())
            except (ValueError, TypeError):
                pass

        # Convert numeric string to int for trashLevel
        if "trashLevel" in converted and converted["trashLevel"] is not None:
            try:
                converted["trashLevel"] = int(str(converted["trashLevel"]).strip())
            except (ValueError, TypeError):
                pass

        # Convert categories to list of integer IDs
        if "categories" in converted and converted["categories"] is not None:
            raw = converted["categories"]
            cleaned = []
            if isinstance(raw, str):
                raw = raw.strip()
                if raw.startswith("[") and raw.endswith("]"):
                    try:
                        cleaned = [int(x) for x in json.loads(raw)]
                    except Exception:
                        cleaned = [int(x.strip()) for x in raw.strip("[]").split(",") if x.strip()]
                elif "," in raw:
                    cleaned = [int(x.strip()) for x in raw.split(",") if x.strip()]
                elif raw.isdigit():
                    cleaned = [int(raw)]
                else:
                    cleaned = [raw]
            elif isinstance(raw, (int, float)):
                cleaned = [int(raw)]
            elif isinstance(raw, (list, tuple)):
                for item in raw:
                    if isinstance(item, str) and "," in item:
                        cleaned.extend([int(x.strip()) for x in item.split(",") if x.strip()])
                    else:
                        try:
                            cleaned.append(int(item))
                        except (ValueError, TypeError):
                            cleaned.append(item)
            converted["categories"] = cleaned

        # Ensure photos is always a list
        if "photos" in converted and not isinstance(converted["photos"], list):
            converted["photos"] = [converted["photos"]]
        elif "photo" in converted and "photos" not in converted:
            converted["photos"] = converted["photo"] if isinstance(converted["photo"], list) else [converted["photo"]]

        return super().to_internal_value(converted)



class DisposalSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source="created_at", format="%d/%m/%Y")
    type = serializers.SerializerMethodField()
    items = serializers.CharField(source="items_description")
    trashLevel = serializers.IntegerField(source="occupancy_level_reported")
    trashCode = serializers.CharField(source="trash_bin.code")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Disposal
        fields = ("id", "date", "type", "quantity", "items", "trashLevel", "trashCode", "image", "points_awarded")

    def get_type(self, obj):
        return ", ".join(obj.categories.values_list("name", flat=True))

    def get_image(self, obj):
        photo = obj.photos.first()
        if not photo:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(photo.image.url) if request else photo.image.url
