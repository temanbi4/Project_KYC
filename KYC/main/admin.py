# main/admin.py
from django.contrib import admin
from .models import Document
from .tasks import approve_documents_async, reject_documents_async
from django.utils.html import format_html


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'status', 'uploaded_at')
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

    def get_status(self, obj):
        """Возвращает статус документа."""
        if obj.is_approved:
            return format_html('<span style="color: green;">Подтвержден</span>')
        elif obj.is_rejected:
            return format_html('<span style="color: red;">Отклонен</span>')
        else:
            return format_html('<span style="color: orange;">Ожидает проверки</span>')

    get_status.short_description = 'Статус'

    @admin.display(ordering='is_approved')
    def status(self, obj):
        return self.get_status(obj)

    approve_documents.short_description = "Подтвердить выбранные документы"
    reject_documents.short_description = "Отклонить выбранные документы"
