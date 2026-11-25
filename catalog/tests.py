"""Тесты приложения catalog."""

from decimal import Decimal
from io import StringIO

from django.contrib import admin
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .forms import ProductForm
from .models import Category, Product


class CatalogViewsTests(TestCase):
    """Проверяет страницы каталога, карточки товаров и форму добавления."""

    def setUp(self):
        self.category = Category.objects.create(
            name="Электроника",
            description="Техника для дома и работы.",
        )
        self.product = Product.objects.create(
            name="Ноутбук Aurora 14",
            description="Лёгкий ноутбук для учёбы и работы: 16 ГБ ОЗУ, SSD 512 ГБ.",
            category=self.category,
            price=Decimal("79990.00"),
        )

    def test_home_page_lists_products(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/home.html")
        self.assertIn("products", response.context)
        self.assertContains(response, self.product.name)
        self.assertContains(response, "79990,00")
        self.assertTemplateUsed(response, "catalog/includes/menu.html")
        self.assertTemplateUsed(response, "catalog/includes/product_card.html")

    def test_home_page_shows_all_products_from_database(self):
        second_product = Product.objects.create(
            name="Смартфон Nova X",
            description="Смартфон с OLED-экраном.",
            category=self.category,
            price=Decimal("49990.00"),
        )

        response = self.client.get(reverse("catalog:home"))

        self.assertQuerySetEqual(
            response.context["products"],
            [self.product, second_product],
            ordered=False,
        )
        self.assertContains(response, second_product.name)

    def test_home_page_truncates_long_description(self):
        self.product.description = "Очень длинное описание " * 10
        self.product.save()

        response = self.client.get(reverse("catalog:home"))

        self.assertNotContains(response, self.product.description)
        self.assertContains(response, self.product.description[:99])

    def test_product_detail_page(self):
        response = self.client.get(
            reverse("catalog:product_detail", args=[self.product.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_detail.html")
        self.assertEqual(response.context["product"], self.product)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, "79990,00")
        self.assertContains(response, self.category.name)

    def test_product_detail_page_returns_404_for_unknown_product(self):
        response = self.client.get(
            reverse("catalog:product_detail", args=[self.product.pk + 1000])
        )

        self.assertEqual(response.status_code, 404)

    def test_product_create_page_shows_form(self):
        response = self.client.get(reverse("catalog:product_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_form.html")
        self.assertIsInstance(response.context["form"], ProductForm)

    def test_product_create_saves_product_to_database(self):
        response = self.client.post(
            reverse("catalog:product_create"),
            {
                "name": "Настольная лампа Loft",
                "description": "Регулируемая лампа с тёплым светом.",
                "category": self.category.pk,
                "price": "2490.00",
            },
            follow=True,
        )

        new_product = Product.objects.get(name="Настольная лампа Loft")
        self.assertRedirects(
            response,
            reverse("catalog:product_detail", args=[new_product.pk]),
        )
        self.assertEqual(new_product.category, self.category)
        self.assertEqual(new_product.price, Decimal("2490.00"))
        self.assertContains(response, "успешно добавлен")

    def test_product_create_shows_errors_and_does_not_save_invalid_data(self):
        response = self.client.post(
            reverse("catalog:product_create"),
            {
                "name": "Но",
                "description": "",
                "category": "",
                "price": "-10",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("description", form.errors)
        self.assertIn("category", form.errors)
        self.assertIn("price", form.errors)

    def test_models_are_registered_in_admin(self):
        self.assertIn(Category, admin.site._registry)
        self.assertIn(Product, admin.site._registry)


class ProductFormTests(TestCase):
    """Проверяет валидацию формы товара."""

    def setUp(self):
        self.category = Category.objects.create(name="Книги")

    def test_valid_form_saves_product(self):
        form = ProductForm(
            data={
                "name": "Чистый код",
                "description": "Книга о разработке программного обеспечения.",
                "category": self.category.pk,
                "price": "1990.00",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        product = form.save()
        self.assertEqual(product.name, "Чистый код")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.price, Decimal("1990.00"))

    def test_required_fields(self):
        form = ProductForm(data={})

        self.assertFalse(form.is_valid())
        for field_name in ("name", "description", "category", "price"):
            self.assertIn(field_name, form.errors)

    def test_price_must_be_positive(self):
        form = ProductForm(
            data={
                "name": "Плед Soft Home",
                "description": "Мягкий плед для дома.",
                "category": self.category.pk,
                "price": "0",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_name_must_not_be_too_short(self):
        form = ProductForm(
            data={
                "name": "Но",
                "description": "Слишком короткое название.",
                "category": self.category.pk,
                "price": "100.00",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


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
