# ✉️ MailDispatch-Core

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📝 Описание

MailDispatch-Core — сервис управления email-рассылками.  
Учебный проект курса «Python-разработчик», реализующий полный цикл создания и выполнения рассылок с разграничением ролей.

**Основные возможности**

- **Рассылки** — создание, редактирование, запуск, отключение и удаление.  
- **Получатели** — ведение базы клиентов с привязкой к создателю.  
- **Сообщения** — шаблоны писем, которые используются в рассылках.  
- **Попытки отправки** — история каждой попытки с фиксацией статуса и ответа сервера.  
- **Роли** — «Пользователь» и «Менеджер» с разделением прав:
  - Пользователь работает только со своими данными.
  - Менеджер видит всё, может блокировать пользователей и отключать чужие рассылки, но не редактировать и не удалять их.
- **Аутентификация** — кастомная модель пользователя (вход по email), верификация через токен, восстановление пароля.  
- **Кеширование** — серверный кеш на Redis для главной страницы, клиентский кеш для статических файлов.

---

## 🛠️ Технологии

- Django 6.0
- Python 3.14
- Poetry
- Bootstrap 5
- PostgreSQL
- Redis
- psycopg2-binary
- python-dotenv
- Pillow

---

## 🚀 Быстрый старт

### Требования

- Python 3.14+
- Poetry
- Git
- PostgreSQL
- Redis (запущенный сервер)

### Установка

1. Клонируйте репозиторий
```
git clone git@github.com:GrandBalaxon/MailDispatch-Core.git
```
```
cd MailDispatch-Core
```

2. Установите зависимости через Poetry
```
poetry install
```

3. Создайте файл окружения из образца
```
cp .env.sample .env
```
 Откройте .env в редакторе и заполните SECRET_KEY, настройки БД, SMTP, REDIS_URL и пр.

4. Убедитесь, что PostgreSQL запущен, и создайте базу данных (если не создана)
 Пример для локального PostgreSQL:
```
createdb maildispatch_db   # или укажите имя из .env
 ```

5. Убедитесь, что Redis запущен
```
redis-server              # если Redis не запущен, запустите его
```

6. Примените миграции
```
python manage.py migrate
```

7. Создайте суперпользователя (email будет логином)
```
python manage.py createsuperuser
```

8. (Опционально) Загрузите тестовые данные из фикстуры
```
python manage.py loaddata core/fixtures/initial_core_data.json
```

9. Запустите сервер разработки
```
python manage.py runserver
```
    

---
   
## 📦 Структура проекта

```
MailDispatch-Core/
│
├── config/                # Конфигурация Django
│
├── users/                 # Приложение «Пользователи»
│   ├── templates/users/   
│   ├── models.py          
│   ├── views.py           
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── core/                  # Основное приложение (рассылки, получатели, сообщения, попытки)
│   ├── templates/core/    
│   ├── fixtures/
│   ├── management/commands/
│   │   └── load_test_data_core.py
│   ├── models.py          
│   ├── views.py           
│   ├── mixins.py          
│   ├── services.py        
│   ├── forms.py           
│   ├── urls.py
│   └── admin.py
│
├── templates/             
├── static/                
├── media/           
├── .env.sample
├── manage.py
├── pyproject.toml
└── README.md
```

---

## 📜 Лицензия

Этот проект распространяется под лицензией MIT.