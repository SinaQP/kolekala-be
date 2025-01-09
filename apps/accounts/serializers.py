import re

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    @staticmethod
    def validate_iranian_phone_number(value):
        pattern = re.compile(r'^(?:\+98|0)?9\d{9}$')
        if not pattern.match(value):
            raise serializers.ValidationError("شماره تلفن نامعتبر است. لطفاً شماره تلفن ایرانی معتبری وارد کنید.")
        return value

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate_phone_number(self, value):
        return UserRegistrationSerializer.validate_iranian_phone_number(value)