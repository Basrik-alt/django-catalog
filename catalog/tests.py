"""Тесты маршрутов и контроллеров приложения catalog."""

from django.test import SimpleTestCase
from django.urls import reverse


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
