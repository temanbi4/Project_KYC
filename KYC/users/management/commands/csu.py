from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from users.models import User


class Command(BaseCommand):
    """
    Комманда для создания супер юзера python manage.py csu
    python manage.py csu --email="Ваша почта администратора" --password="Ваш пароль администратора"
    """

    def add_arguments(self, parser):
        """Использование аргументов для кастомных данных авторизации администратора"""
        parser.add_argument('--email', type=str, help='Email address for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        """Создаем админа"""
        email = options['email'] or "colombodoro@ya.ru"
        password = options['password'] or "admin"

        try:
            user = User.objects.create(
                email=email,
                is_staff=True,
                is_superuser=True,
            )

            user.set_password(password)
            user.save()
            print("SuperUser created")

        except IntegrityError as e:
            print("Такой пользователь уже существует")