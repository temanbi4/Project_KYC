# main/views.py
from django.core.mail import send_mail
from rest_framework import generics, permissions
from KYC.settings import EMAIL_HOST_USER
from main.models import Document
from main.serializers import (
    DocumentSerializer,
    DocumentListSerializer,
    DocumentCheckSerializer,
    DocumentIdSerializer,
    DocumentAllSerializer
)
from users.models import User
from .utils import send_approval_notification, send_rejection_notification


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Пользователи имеют доступ только к своим собственным объектам.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class DocumentCreateAPIView(generics.CreateAPIView):
    """
    API-представление для создания (загрузки) документа.
    Пользователь должен быть аутентифицирован для использования этого API.
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Выполняет сохранение объекта после загрузки файла.
        Пользователь, загрузивший файл, присваивается как владелец документа.
        Отправляется уведомление администратору о новом документе.
        """
        document = serializer.save(user=self.request.user)
        admin_users = User.objects.filter(is_staff=True)
        admin_email = admin_users.first().email

        send_mail(
            subject='Новый документ',
            message=f'Новый документ был загружен {self.request.user.uploaded_at} '
                    f'пользователем {self.request.user.email}. Подтвердите его в админке.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[admin_email]
        )

        return document


class DocumentListAPIView(generics.ListAPIView):
    """
    API-представление для просмотра списка загруженных документов.
    Пользователь должен быть аутентифицирован для использования этого API.
    """
    serializer_class = DocumentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает только документы, загруженные текущим пользователем."""
        return Document.objects.filter(user=self.request.user)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API-представление для просмотра, изменения и удаления данных о документе.
    Пользователь должен быть аутентифицирован для использования этого API.
    """
    serializer_class = DocumentAllSerializer
    queryset = Document.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def perform_update(self, serializer):
        """
        Выполняет обновление данных о документе.
        Отправляет уведомление пользователю после подтверждения документа или отклонения.
        """
        document = serializer.save()

        # Сбросим флаг is_rejected, если документ подтвержден
        if document.is_approved:
            document.is_rejected = False
            document.save()
            send_approval_notification([document])
        # Сбросим флаг is_approved, если документ отклонен
        elif document.is_rejected:
            document.is_approved = False
            document.save()
            send_rejection_notification([document])