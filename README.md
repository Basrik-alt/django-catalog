# Django Catalog

Учебный проект на Django: сайт-каталог с главной страницей и страницей контактов.

## Описание

Проект демонстрирует базовую структуру Django-приложения:

- создание и настройка Django-проекта;
- создание приложения `catalog` и его регистрация в `INSTALLED_APPS`;
- подключение URL-адресов приложения через `include`;
- контроллеры на основе функции `render`;
- HTML-шаблоны с наследованием и стилями Bootstrap 5.

## Стек

- Python 3.12+
- Django 6.0
- Bootstrap 5 (CDN)
- SQLite (база данных по умолчанию)

## Структура проекта

```text
django-catalog/
├── catalog/                  # приложение каталога
│   ├── templates/catalog/    # HTML-шаблоны приложения
│   │   ├── base.html         # общий каркас страниц
│   │   ├── home.html         # главная страница
│   │   └── contacts.html     # страница контактов
│   ├── tests.py              # тесты контроллеров
│   ├── urls.py               # маршруты приложения
│   └── views.py              # контроллеры
├── catalog_project/          # настройки Django-проекта
│   ├── settings.py
│   └── urls.py               # корневая маршрутизация
├── static/css/style.css      # пользовательские стили
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Запуск проекта

1. Клонируйте репозиторий и перейдите в его директорию:

   ```bash
   git clone https://github.com/Basrik-alt/django-catalog.git
   cd django-catalog
   ```

2. Создайте и активируйте виртуальное окружение:

   **Windows (PowerShell):**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции:

   ```bash
   python manage.py migrate
   ```

5. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

6. Откройте в браузере:

   - главная страница — <http://127.0.0.1:8000/>
   - контакты — <http://127.0.0.1:8000/contacts/>
   - админка — <http://127.0.0.1:8000/admin/>

## Маршруты

| URL          | Контроллер           | Шаблон                 |
| ------------ | -------------------- | ---------------------- |
| `/`          | `catalog.views.home` | `catalog/home.html`    |
| `/contacts/` | `catalog.views.contacts` | `catalog/contacts.html` |

## Тесты

```bash
python manage.py test
```

## Git workflow

В проекте используется модель GitFlow:

- `main` — стабильная версия проекта;
- `develop` — ветка для интеграции изменений;
- `homework/django-catalog` — ветка с выполнением домашнего задания;
- изменения попадают в `develop` через pull request.
