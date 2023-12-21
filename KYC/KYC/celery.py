from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KYC.settings')

# Создание экземпляра Celery
celery_app = Celery('KYC')

# Загрузка настроек из конфигурационного файла Django
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из приложений Django
celery_app.autodiscover_tasks()
