"""Тесты приложения catalog."""

from decimal import Decimal
from io import StringIO

from django.contrib import admin
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogViewsTests(SimpleTestCase):
    """Проверяет, что страницы каталога доступны и используют нужные шаблоны."""

    def test_home_page(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/home.html")

    def test_contacts_page(self):
        response = self.client.get(reverse("catalog:contacts"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/contacts.html")

    def test_models_are_registered_in_admin(self):
        self.assertIn(Category, admin.site._registry)
        self.assertIn(Product, admin.site._registry)


class CatalogModelsTests(TestCase):
    """Проверяет модели и связи каталога."""

    def setUp(self):
        self.category = Category.objects.create(
            name="Электроника",
            description="Техника для дома и работы.",
        )
        self.product = Product.objects.create(
            name="Ноутбук",
            description="Ноутбук для учёбы.",
            category=self.category,
            price=Decimal("79990.00"),
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Электроника")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Ноутбук")

    def test_product_belongs_to_category(self):
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.products.all())


class LoadTestDataCommandTests(TestCase):
    """Проверяет кастомную команду загрузки тестовых данных."""

    def test_command_clears_old_data_and_loads_fixtures(self):
        old_category = Category.objects.create(name="Старая категория")
        Product.objects.create(
            name="Старый продукт",
            category=old_category,
            price=Decimal("100.00"),
        )

        call_command("load_test_data", stdout=StringIO())

        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Product.objects.count(), 6)
        self.assertFalse(Category.objects.filter(name="Старая категория").exists())
        self.assertTrue(Product.objects.filter(category__name="Книги").exists())
