from KYC.celery import app as celery_app

__all__ = ("celery_app",)

celery_app.autodiscover_tasks()
