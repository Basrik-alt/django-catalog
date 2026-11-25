"""Контроллеры приложения catalog."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def home(request):
    """Отображает главную страницу со всеми товарами каталога."""
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


def contacts(request):
    """Отображает страницу с контактной информацией."""
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    """Показывает подробную информацию о товаре по его первичному ключу."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def product_create(request):
    """Показывает форму и сохраняет новый товар в базу данных."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request,
                f"Товар «{product.name}» успешно добавлен в каталог.",
            )
            return redirect("catalog:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})
