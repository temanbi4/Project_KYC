from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from users.models import User


class Command(BaseCommand):
    """Комманда для создания супер юзера python manage.py csu """

    def handle(self, *args, **options):
        """Создаем админа"""
        try:
            user = User.objects.create(
                email='admin@admin.admin',
                is_staff=True,
                is_superuser=True,
            )

            user.set_password('admin')
            user.save()
            print('SuperUser created')

        except IntegrityError as e:
            print('Такой пользователь уже существует')