# Django Catalog

Учебный сайт-каталог на Django с главной страницей и страницей контактов.

## Краткое описание

**Django Catalog** — учебный веб-проект, который демонстрирует базовую структуру
приложения на Django. На сайте есть главная страница с категориями каталога и
страница с контактной информацией. Проект можно использовать как стартовый
шаблон для дальнейшей разработки.

## Что реализовано

- Django-проект `catalog_project` и приложение `catalog`;
- регистрация приложения в `INSTALLED_APPS`;
- маршрутизация через `catalog/urls.py` и `include` в корневом `urls.py`;
- контроллеры `home` и `contacts` на основе функции `render`;
- HTML-шаблоны с наследованием от `base.html`;
- адаптивное оформление на Bootstrap 5 и собственные стили;
- тесты доступности страниц и используемых шаблонов.

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

## Требования

- Python 3.12 или новее;
- pip;
- Git.

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
