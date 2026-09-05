from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.permissions import IsManagerOrAdmin
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related("trash_bin").order_by("-created_at")


class NotificationReadView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def patch(self, request, pk):
        notification = generics.get_object_or_404(Notification.objects.filter(recipient=request.user), pk=pk)
        notification.read_at = timezone.now()
        notification.save(update_fields=["read_at", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)
