# PostgreSQL Setup Instructions

## 1. Установка PostgreSQL

### Windows:
- Скачайте с https://www.postgresql.org/download/windows/
- Установите с паролем администратора `postgres`

### Или через Chocolatey:
```bash
choco install postgresql
```

## 2. Создание базы данных

После установки откройте **SQL Shell (psql)** и выполните:

```sql
-- Войдите как postgres
-- Создайте базу данных
CREATE DATABASE navis_db;

-- Создайте пользователя
CREATE USER navis_user WITH PASSWORD 'navis_password';

-- Дайте права
GRANT ALL PRIVILEGES ON DATABASE navis_db TO navis_user;

-- Выйдите
\q
```

## 3. Настройка Django

Раскомментируйте PostgreSQL настройки в `config/settings.py`:

```python
# PostgreSQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'navis_db'),
        'USER': os.environ.get('DB_USER', 'navis_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'navis_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## 4. Применение миграций

```bash
.\venv\Scripts\python.exe manage.py migrate
```

## 5. Проверка подключения

```bash
.\venv\Scripts\python.exe manage.py runserver
```

## Troubleshooting

### Ошибка "Connection refused":
- Убедитесь что PostgreSQL сервер запущен
- Проверьте порт 5432 в Services.msc

### Ошибка кодировки:
- Убедитесь что база создана с кодировкой UTF8
- Пересоздайте базу: `DROP DATABASE navis_db; CREATE DATABASE navis_db WITH ENCODING 'UTF8';`
