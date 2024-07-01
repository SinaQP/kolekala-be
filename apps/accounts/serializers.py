from rest_framework import serializers

from apps.core.serializers import Serializer


class LoginSerializer(Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False, read_only=True)


class SignUpSerializer(Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=False, read_only=True)


