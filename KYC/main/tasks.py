# main/tasks.py
from celery import shared_task
from main.utils import approve_documents, reject_documents, send_new_document_notification
from main.models import Document
from . import tasks


@shared_task
def approve_documents_async(document_ids):
    """Асинхронное подтверждение документов."""
    approve_documents(document_ids)


@shared_task
def reject_documents_async(document_ids):
    """Асинхронное отклонение документов."""
    reject_documents(document_ids)


@shared_task
def async_send_new_document_notification(document_id):
    """Asynchronous sending of notification for a new document."""
    document = Document.objects.get(id=document_id)
    send_new_document_notification(document)