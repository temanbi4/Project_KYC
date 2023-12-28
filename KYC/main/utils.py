# main/utils.py
from celery import shared_task
from django.core.mail import send_mail
from KYC.settings import EMAIL_HOST_USER
from main.models import Document
from users.models import User


# Быстрое действие для подтверждения документов.
@shared_task
def approve_documents(document_ids):
    documents = Document.objects.filter(id__in=document_ids)
    for document in documents:
        document.is_approved = True
        document.save()
        send_approval_notification.apply_async(args=[document.id])


# Быстрое действие для отклонения документов.
@shared_task
def reject_documents(document_ids):
    documents = Document.objects.filter(id__in=document_ids)
    for document in documents:
        document.is_rejected = True
        document.save()
        send_rejection_notification.apply_async(args=[document.id])


# Отправляет уведомление пользователю после подтверждения документа.
@shared_task
def send_approval_notification(document_id):
    document = Document.objects.get(id=document_id)
    send_mail(
        subject='Документ подтвержден',
        message=f'Ваш документ был подтвержден администратором.',
        from_email=EMAIL_HOST_USER,
        recipient_list=[document.user.email]
    )


# Отправляет уведомление пользователю после отклонения документа.
@shared_task
def send_rejection_notification(document_id):
    document = Document.objects.get(id=document_id)
    send_mail(
        subject='Документ отклонен',
        message=f'Ваш документ был отклонен администратором. Пожалуйста, проверьте и отправьте заново.',
        from_email=EMAIL_HOST_USER,
        recipient_list=[document.user.email]
    )


@shared_task
def send_new_document_notification(document_id):
    """
    Отправляет уведомление администратору о новом документе.
    """
    document = Document.objects.get(id=document_id)
    admin_users = User.objects.filter(is_staff=True)
    admin_email = admin_users.first().email

    send_mail(
        subject='Новый документ',
        message=f'Новый документ "{document.file.name}" был загружен {document.uploaded_at} '
                f'пользователем {document.user.email}. Подтвердите его в админке.',
        from_email=EMAIL_HOST_USER,
        recipient_list=[admin_email]
    )
