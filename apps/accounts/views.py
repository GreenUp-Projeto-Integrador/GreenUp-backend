from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.disposals.models import Disposal, PointsTransaction
from .models import User
from .permissions import IsAdministrator
from .serializers import ChangePasswordSerializer, RegisterSerializer, UserSerializer
from .services import change_password, reactivate_user, suspend_user


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        change_password(request.user, serializer.validated_data["currentPassword"], serializer.validated_data["newPassword"])
        return Response({"success": True, "message": "Senha alterada com sucesso."})


class AccountSummaryView(APIView):
    def get(self, request):
        points = PointsTransaction.objects.filter(user=request.user).aggregate(total=Sum("points"))["total"] or 0
        count = Disposal.objects.filter(user=request.user).count()
        level = "Ouro" if points >= 1000 else "Prata" if points >= 500 else "Bronze"
        return Response({"name": request.user.name, "email": request.user.email, "joinDate": request.user.date_joined.date(), "points": points, "level": level, "disposalsCount": count})


class UserStatusView(APIView):
    permission_classes = [IsAdministrator]

    def post(self, request, pk, action):
        user = get_object_or_404(User, pk=pk)
        if action == "suspend":
            suspend_user(user)
        elif action == "reactivate":
            reactivate_user(user)
        else:
            raise NotFound("Ação administrativa não encontrada.")
        return Response(status=status.HTTP_204_NO_CONTENT)
