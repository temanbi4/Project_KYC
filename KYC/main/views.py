from rest_framework import generics, permissions
from main.models import Document
from .utils import (
    send_approval_notification,
    send_rejection_notification,
    send_new_document_notification,
)
from main.serializers import (
    DocumentSerializer,
    DocumentListSerializer,
    DocumentAllSerializer,
)


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

        send_new_document_notification.apply_async(args=[document.id])

        return document


class DocumentListAPIView(generics.ListAPIView):
    """
    API-представление для просмотра списка загруженных документов.
    Пользователь должен быть аутентифицирован для использования этого API.
    """

    serializer_class = DocumentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает только документы, загруженные текущим пользователем.
           Администратору возращает все загруженные документы.
        """
        user = self.request.user
        if user.is_staff:  # Проверяем, является ли пользователь администратором
            return (
                Document.objects.all()
            )  # Если администратор, то возвращаем все документы
        else:
            return Document.objects.filter(
                user=user
            )  # Возвращаем документы пользователя


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

        # Сброс флага is_rejected, если документ подтвержден
        if document.is_approved:
            document.is_rejected = False
            document.save()
            send_approval_notification.apply_async(
                args=[document.id], serializer="json", encoder="DjangoJSONEncoder"
            )
        # Сброс флаг is_approved, если документ отклонен
        elif document.is_rejected:
            document.is_approved = False
            document.save()
            send_rejection_notification.apply_async(
                args=[document.id], serializer="json", encoder="DjangoJSONEncoder"
            )
