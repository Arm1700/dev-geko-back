import os
from django.core.management.base import BaseCommand
import subprocess
from datetime import datetime
import environ

# Инициализация environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
environ.Env.read_env()

# Инициализация переменных окружения
env = environ.Env()

class Command(BaseCommand):
    help = 'Create a backup of the database and media files'

    def handle(self, *args, **kwargs):
        # Получаем значение поддомена из .env
        subdomain = env('SUBDOMAIN', default='default')

        # Дата создания
        date_folder = datetime.now().strftime("%Y-%m-%d")

        # Путь для бэкапов: SUBDOMAIN/backups/DATE
        backup_dir = os.path.abspath(os.path.join(BASE_DIR, '..', '..', subdomain, 'backups', date_folder))
        media_dir = os.path.join(BASE_DIR, 'media')  # Директория с медиа-файлами

        # Создание директории для бэкапов, если её нет
        os.makedirs(backup_dir, exist_ok=True)

        # Форматирование имени файлов с текущей датой и временем
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.sql")
        media_backup_file = os.path.join(backup_dir, f"media_backup_{timestamp}.tar.gz")

        # Бэкап базы данных
        self.stdout.write("Backing up the database...")
        subprocess.run(
            ["pg_dump", "-U", env('DB_USER'), "-h", "localhost", "-p", "5432", env('DB_NAME')],
            stdout=open(db_backup_file, "w"),
            check=True,
        )

        # Бэкап медиа файлов
        self.stdout.write("Backing up media files...")
        subprocess.run(
            ["tar", "-czvf", media_backup_file, "-C", media_dir, "."],
            check=True,
        )

        self.stdout.write(f"Backup completed! Files saved to {backup_dir}")
