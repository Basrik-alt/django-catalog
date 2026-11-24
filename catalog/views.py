"""Контроллеры приложения catalog."""

from django.shortcuts import render


def home(request):
    """Отображает главную страницу каталога."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Отображает страницу с контактной информацией."""
    return render(request, "catalog/contacts.html")
