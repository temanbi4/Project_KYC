from rest_framework import serializers
from main.models import Document
from users.serializers import UserDocSerializer


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания (загрузки документа)"""

    class Meta:
        model = Document
        fields = ["file"]


class DocumentListSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра отправленных файлов"""

    user = UserDocSerializer(read_only=True)  # вложенный сериализатор

    class Meta:
        model = Document
        fields = ["id", "user", "file", "is_approved", "is_rejected", "uploaded_at"]

    def update_document_status(self, instance, is_approved, is_rejected):
        """Метод для обновления статуса документа"""
        instance.is_approved = is_approved
        instance.is_rejected = is_rejected
        instance.save()
        return instance


class DocumentCheckSerializer(serializers.ModelSerializer):
    """Сериализатор для админов на принятие или отклонение документа"""

    user = UserDocSerializer(read_only=True)  # вложенный сериализатор

    class Meta:
        model = Document
        fields = ["id", "is_approved", "is_rejected", "user"]


class DocumentIdSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления документов"""

    class Meta:
        model = Document
        fields = []


class DocumentAllSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра данных каждого документа отдельно"""

    user = UserDocSerializer(read_only=True)  # вложенный сериализатор

    class Meta:
        model = Document
        fields = "__all__"
