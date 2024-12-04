import csv
import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Генерирует 100 пользователей и сохраняет их в CSV файл'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Путь к CSV файлу для сохранения пользователей',
            default='generated_users.csv'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        users_data = []

        for i in range(1, 101):
            username = f'user{i}'
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            users_data.append({'username': username, 'password': password})

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
                self.stdout.write(self.style.SUCCESS(f'Пользователь {username} создан'))
            else:
                self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует'))

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['username', 'password'])
                writer.writeheader()
                writer.writerows(users_data)
                self.stdout.write(self.style.SUCCESS(f'Данные пользователей сохранены в {file_path}'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при записи в CSV файл: {e}'))