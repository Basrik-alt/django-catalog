"""Формы приложения catalog."""

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма добавления товара в каталог.

    Все значимые поля обязательны, цена проверяется на положительное значение,
    а название — на минимальную длину. Данные сохраняются в базу через
    ``ModelForm.save()``.
    """

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, Ноутбук Aurora 14",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Расскажите о товаре: характеристики, комплектация, особенности.",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "0.00",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # В модели описание необязательное, но в форме оно нужно для карточки товара.
        self.fields["description"].required = True
        for field_name in ("name", "description", "category", "price"):
            self.fields[field_name].required = True

    def clean_name(self):
        """Проверяет, что название не слишком короткое."""
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Название должно содержать не менее 3 символов.")
        return name

    def clean_price(self):
        """Проверяет, что цена положительная."""
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля.")
        return price
