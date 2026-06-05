# Настройка проекта TeamFinder

## 1. Виртуальное окружение

Перед началом работы необходимо создать и активировать виртуальное окружение Python.  

1. **Создайте виртуальное окружение (в папке проекта):**
   ```bash
   python3 -m venv venv
   ```

2. **Активируйте окружение:**

    - **Windows (PowerShell):**
      ```bash
      venv\Scripts\Activate.ps1
      ```
    - **Windows (cmd):**
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

3. **Установите зависимости из `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

## 2. Создание `.env`

Файл `.env` содержит конфиденциальные настройки проекта — ключ Django, параметры БД и другие переменные.  

В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```

После этого откройте `.env` и укажите свои значения.  

| Переменная            | Назначение                                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG**      | Режим отладки. Установите `True` во время разработки.                                                                                                      |
| **POSTGRES_DB**       | Имя базы данных PostgreSQL, которую будет использовать Django.                                                                                             |
| **POSTGRES_USER**     | Имя пользователя PostgreSQL.                                                                                                                               |
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.                                                                                                                            |
| **POSTGRES_HOST**     | Адрес сервера БД. В случае локальной разработки localhost.                                                                                                 |
| **POSTGRES_PORT**     | Порт подключения к БД (по умолчанию `5432`).                                                                                                               |

---

## 3. Запуск PostgreSQL

Для работы приложения **TeamFinder** используется база данных **PostgreSQL**.
По условию задания база данных должна запускаться в контейнере Docker.

В проекте уже есть пример файла `docker-compose.yml`. Запустите контейнер:

```bash
docker compose up -d
```

Проверьте, что контейнер работает:

```bash
docker ps
```

Остановить контейнер можно командой:
```bash
docker compose down
```

Если возникает ошибка "permission denied while trying to connect to the Docker daemon socket", то может потребоваться добавить `sudo` перед командой.
> Если порт 5432 уже занят, измените левую часть в ports в docker-compose.yml (например, "5433:5432") и укажите этот порт в .env (POSTGRES_PORT=5433).


## 4. Миграции базы данных

После запуска PostgreSQL примените миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Создание суперпользователя (администратора)
Для доступа в административную панель создайте суперпользователя:

```bash
python manage.py createsuperuser
```
Будут запрошены email, имя, фамилия, телефон (можно указать +70000000000) и пароль.


## 6. Запуск сервера разработки

```bash
python manage.py runserver
```

Теперь проект доступен по адресу [http://localhost:8000](http://localhost:8000). 

- Главная страница — редирект на /projects/list/ (список проектов)
- Страницы пользователей: /users/list/, /users/<id>/
- Регистрация и вход: /users/register/, /users/login/
- Управление проектами: /projects/create-project/, /projects/<id>/edit/
- Автодополнение навыков: /projects/skills/?q=...
- Добавление/удаление навыков: /projects/<id>/skills/add/, /projects/<id>/skills/<skill_id>/remove/
