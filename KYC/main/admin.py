# main/admin.py
from django.contrib import admin
from .models import Document
from .utils import approve_documents, reject_documents, send_rejection_notification, send_approval_notification


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'is_approved', 'is_rejected', 'uploaded_at')
    list_filter = ('is_approved', 'is_rejected')
    search_fields = ('user__email', 'file')
    actions = ['approve_documents', 'reject_documents']

    def approve_documents(self, request, queryset):
        """Быстрое действие для подтверждения документов."""
        queryset.update(is_approved=True)
        send_approval_notification(queryset)

    def reject_documents(self, request, queryset):
        """Быстрое действие для отклонения документов."""
        queryset.update(is_rejected=True)
        send_rejection_notification(queryset)

    approve_documents.short_description = "Подтвердить выбранные документы"
    reject_documents.short_description = "Отклонить выбранные документы"
