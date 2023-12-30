from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main.utils import send_new_document_notification


class DocumentTest(TestCase):
    def setUp(self):
        # Добавляем Юзера
        self.user = get_user_model().objects.create(
            email='test@example.com',
            password='testpassword',
        )
        # Добавляем администратора
        self.admin_user = get_user_model().objects.create(
            email='admin@example.com',
            password='adminpassword',
            is_staff=True,
            is_superuser=True,
        )
        self.admin_user.save()
        self.client = APIClient()

    def test_document_creation(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Формируем тестовый файл
        file_content = b"file_content"
        test_file = SimpleUploadedFile("test.txt", file_content)

        # Создаем объект Document вручную с определенным идентификатором
        document_id = 1  # или любое другое значение, которое вы хотите использовать
        document = Document(id=document_id, file=test_file, user=self.user)

        # Данные для POST-запроса
        data = {'file': test_file}

        # Выполнение POST-запроса
        response = self.client.post(reverse('main:document-create'), data, format='multipart')

        # Проверка корректного ответа и создания объекта
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)

        # Получаем объект Document после сохранения
        document = Document.objects.first()

        # Посылаем уведомление асинхронно, используя document_info вместо document.id
        send_new_document_notification.apply_async(args=[document_id])

        # Проверка, что атрибут user объекта совпадает с текущим пользователем
        self.assertEqual(document.user, self.user)