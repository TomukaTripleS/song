from collections.abc import Mapping

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(
        write_only=True, min_length=8, max_length=128, trim_whitespace=False
    )
    password_confirmation = serializers.CharField(
        write_only=True, max_length=128, trim_whitespace=False
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "password", "password_confirmation",
        ]
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        if isinstance(data, Mapping):
            username = data.get("username")
            if isinstance(username, str):
                data = data.copy()
                data["username"] = User.normalize_username(username)
        return super().to_internal_value(data)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Паролі не збігаються."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        return User.objects.create_user(**validated_data)
