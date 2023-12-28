# main/admin.py
from django.contrib import admin
from .models import Document
from .utils import approve_documents, reject_documents, send_rejection_notification, send_approval_notification
from .tasks import approve_documents_async, reject_documents_async


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'is_approved', 'is_rejected', 'uploaded_at')
    list_filter = ('is_approved', 'is_rejected')
    search_fields = ('user__email', 'file')
    actions = ['approve_documents', 'reject_documents']

    def approve_documents(self, request, queryset):
        """Быстрое действие для подтверждения документов."""
        document_ids = queryset.values_list('id', flat=True)
        approve_documents_async.apply_async(args=[list(document_ids)])

    def reject_documents(self, request, queryset):
        """Быстрое действие для отклонения документов."""
        document_ids = queryset.values_list('id', flat=True)
        reject_documents_async.apply_async(args=[list(document_ids)])

    approve_documents.short_description = "Подтвердить выбранные документы"
    reject_documents.short_description = "Отклонить выбранные документы"
