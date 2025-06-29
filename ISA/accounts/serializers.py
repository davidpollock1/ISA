from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import transaction
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])

        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data["user"] = user
        return data


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=6, write_only=True)
    re_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    city = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("re_password")

        profile_fields = ["first_name", "last_name", "phone", "city", "email"]
        profile_data = {key: validated_data.pop(key, "") for key in profile_fields}

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, **profile_data)

        return user
