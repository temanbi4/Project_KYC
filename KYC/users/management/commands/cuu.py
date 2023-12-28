from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from users.models import User


class Command(BaseCommand):
    """Комманда для создания юзера python manage.py cuu """

    def handle(self, *args, **options):
        """Создаем юзера"""
        try:
            user = User.objects.create(
                email='colombadoro@ya.ru',
                is_staff=False,
                is_superuser=False,
            )

            user.set_password('admin')
            user.save()
            print('User created')

        except IntegrityError as e:
            print('Такой пользователь уже существует')