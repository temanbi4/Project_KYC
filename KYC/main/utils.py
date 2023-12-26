# main/utils.py
from django.core.mail import send_mail
from KYC.settings import EMAIL_HOST_USER


def approve_documents(documents):
    """Быстрое действие для подтверждения документов."""
    for document in documents:
        document.is_approved = True
        document.save()


def reject_documents(documents):
    """Быстрое действие для отклонения документов."""
    for document in documents:
        document.is_rejected = True
        document.save()
        send_rejection_notification([document])


def send_approval_notification(documents):
    """Отправляет уведомление пользователю после подтверждения документа."""
    for document in documents:
        send_mail(
            subject='Документ подтвержден',
            message=f'Ваш документ был подтвержден администратором.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[document.user.email]
        )


def send_rejection_notification(documents):
    """Отправляет уведомление пользователю после отклонения документа."""
    for document in documents:
        send_mail(
            subject='Документ отклонен',
            message=f'Ваш документ был отклонен администратором. Пожалуйста, проверьте и отправьте заново.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[document.user.email]
        )
