from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    trashCode = serializers.CharField(source="trash_bin.code", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    readAt = serializers.DateTimeField(source="read_at", read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "notification_type", "message", "trashCode", "createdAt", "readAt")
