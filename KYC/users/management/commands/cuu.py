from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from users.models import User


class Command(BaseCommand):
    """Команда для создания пользователя python manage.py cuu"""

    def add_arguments(self, parser):
        """Использование аргументов для кастомных данных пользователя"""
        parser.add_argument('--email', type=str, help='Email address for the user')
        parser.add_argument('--password', type=str, help='Password for the user')

    def handle(self, *args, **options):
        """Создаем пользователя"""
        email = options['email'] or "test@test.test"
        password = options['password'] or "test"

        try:
            user = User.objects.create(
                email=email,
                is_staff=False,
                is_superuser=False,
            )

            user.set_password(password)
            user.save()
            print("User created")

        except IntegrityError as e:
            print("Такой пользователь уже существует")
