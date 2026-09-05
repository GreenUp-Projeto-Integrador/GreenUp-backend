from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "confirmPassword")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirmPassword"):
            raise serializers.ValidationError({"confirmPassword": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    zipCode = serializers.CharField(source="zip_code", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "cpf", "address", "city", "state", "zipCode", "role")
        read_only_fields = ("id", "role")


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["newPassword"] != attrs["confirmPassword"]:
            raise serializers.ValidationError({"confirmPassword": "As senhas não coincidem."})
        return attrs
