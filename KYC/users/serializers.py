from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания юзера"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'telegram_id', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password:
            validate_password(password)
            instance.set_password(password)

        instance.save()
        return instance


class UserDocSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения юзера"""
    class Meta:
        model = User
        fields = ['email', 'telegram_id']
