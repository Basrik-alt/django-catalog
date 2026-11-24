"""Кастомная команда для загрузки тестовых данных каталога."""

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Category, Product


class Command(BaseCommand):
    """Очищает каталог и загружает категории и продукты из фикстур."""

    help = "Удаляет существующие данные и загружает тестовые категории и продукты."

    @transaction.atomic
    def handle(self, *args, **options):
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()

        self.stdout.write(
            f"Удалено объектов: продуктов — {deleted_products}, "
            f"категорий — {deleted_categories}."
        )

        call_command("loaddata", "categories.json", verbosity=0)
        call_command("loaddata", "products.json", verbosity=0)

        self.stdout.write(
            self.style.SUCCESS(
                f"Загрузка завершена: категорий — {Category.objects.count()}, "
                f"продуктов — {Product.objects.count()}."
            )
        )
