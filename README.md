# 🏭 Система учёта станков

Веб-приложение для централизованного учёта станочного парка предприятия.

## Технологический стек

| Компонент | Технология |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Frontend | Vue.js 3 + Tailwind CSS |
| База данных | PostgreSQL 15 |
| Кэш | Redis 7 |
| Веб-сервер | Nginx |
| Контейнеризация | Docker + Docker Compose |
| API документация | Swagger (drf-spectacular) |

## Роли пользователей

| Роль | Права |
|---|---|
| **Администратор** | Полный доступ: пользователи, справочники, все операции, журнал аудита |
| **Мастер** | Реестр станков (CRUD), статусы, закрепление операторов, отчёты |
| **Оператор** | Просмотр карточек, добавление отметок статуса своего станка |

---

## Быстрый старт (Docker)

```bash
# 1. Клонировать репозиторий
git clone <repo-url> machine-registry
cd machine-registry

# 2. Создать .env файл
cp .env.example .env
# Отредактируйте .env при необходимости

# 3. Запустить
docker-compose up -d

# 4. Открыть в браузере
# Приложение: http://localhost
# API docs:   http://localhost/api/docs/
# Admin:      http://localhost/admin/
```

**По умолчанию:** логин `admin`, пароль `Admin1234`

---

## Локальная разработка

### Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или: venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать .env
cp ../.env.example .env
# Укажите DB_HOST=localhost

# Применить миграции и заполнить БД
python manage.py migrate
python manage.py seed_db

# Запустить сервер
python manage.py runserver
```

API: http://localhost:8000  
Swagger UI: http://localhost:8000/api/docs/  
ReDoc: http://localhost:8000/api/redoc/

### Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev-сервер
npm run dev
```

Приложение: http://localhost:5173

---

## API Документация

После запуска доступна по адресам:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`
- **OpenAPI Schema:** `/api/schema/`

### Основные эндпоинты

```
POST   /api/v1/auth/login/          — вход в систему
POST   /api/v1/auth/refresh/        — обновление токена
POST   /api/v1/auth/logout/         — выход
GET    /api/v1/auth/me/             — профиль текущего пользователя

GET    /api/v1/machines/            — реестр станков
POST   /api/v1/machines/            — добавить станок
GET    /api/v1/machines/{id}/       — карточка станка
PATCH  /api/v1/machines/{id}/       — обновить станок
DELETE /api/v1/machines/{id}/       — мягкое удаление
POST   /api/v1/machines/{id}/change-status/    — сменить статус
POST   /api/v1/machines/{id}/upload/           — загрузить файл
POST   /api/v1/machines/{id}/assign-operator/  — закрепить оператора
GET    /api/v1/machines/export-excel/          — экспорт в Excel
POST   /api/v1/machines/import-excel/          — импорт из Excel
GET    /api/v1/machines/import-template/       — шаблон импорта

GET    /api/v1/statuses/            — справочник статусов
GET    /api/v1/machine-types/       — типы станков
GET    /api/v1/workshops/           — цеха
GET    /api/v1/employees/           — сотрудники
GET    /api/v1/users/               — пользователи (admin)
GET    /api/v1/audit/               — журнал аудита (admin)
```

---

## Структура проекта

```
machine-registry/
├── backend/
│   ├── apps/
│   │   ├── users/          # Пользователи, JWT-аутентификация
│   │   ├── machines/       # Реестр станков, статусы, файлы
│   │   ├── workshops/      # Цеха и участки
│   │   ├── employees/      # Сотрудники
│   │   └── audit/          # Журнал действий
│   ├── config/             # Настройки Django
│   ├── utils/              # Пермишены, пагинация, middleware
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/          # Страницы приложения
│   │   ├── components/     # Переиспользуемые компоненты
│   │   ├── store/          # Pinia stores
│   │   ├── api/            # API-клиент (axios)
│   │   ├── router/         # Vue Router + guards
│   │   └── assets/         # CSS, шрифты
│   └── package.json
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── .env.example
```

---

## Безопасность

- Пароли хранятся в виде Argon2 хэша
- JWT-токены с 8-часовым сроком жизни
- Blacklist для отозванных refresh-токенов
- CSRF/XSS защита на уровне Django
- CORS настроен только для разрешённых origin
- Мягкое удаление — данные не теряются
- Журнал аудита всех изменений

---

## Резервное копирование

```bash
# Бэкап БД
docker exec machine_registry_db pg_dump -U postgres machine_registry > backup_$(date +%Y%m%d).sql

# Восстановление
docker exec -i machine_registry_db psql -U postgres machine_registry < backup_20240101.sql
```

---

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `SECRET_KEY` | Django секретный ключ | — (обязательно в prod) |
| `DEBUG` | Режим отладки | `False` |
| `DB_NAME` | Имя БД | `machine_registry` |
| `DB_USER` | Пользователь БД | `postgres` |
| `DB_PASSWORD` | Пароль БД | `postgres` |
| `DB_HOST` | Хост БД | `localhost` |
| `REDIS_URL` | URL Redis | `redis://127.0.0.1:6379/1` |
| `TIME_ZONE` | Временная зона | `Asia/Tashkent` |
| `CORS_ALLOWED_ORIGINS` | Разрешённые CORS origin | `http://localhost:3000` |

---

## Лицензия

Proprietary — все права защищены.
