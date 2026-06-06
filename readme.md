# TeamFinder

## Настройка проекта
### 0. Клонирование репозитория и переход в папку проекта
В первую очередь, необходимо склонировать репозиторий
```bash
git clone git@github.com:frlsua/team-finder-ad.git
```
И перейти в папку проекта
```bash
cd team-finder-ad
```

### 1. Виртуальное окружение

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

### 2. Создание `.env`

Файл `.env` содержит конфиденциальные настройки проекта — ключ Django, параметры БД и другие переменные.  

В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```

После этого откройте `.env` и укажите свои значения.  

| Переменная | Назначение | 
| - | - |
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG** | Режим отладки. Установите `True` во время разработки.|
| **POSTGRES_DB** | Имя базы данных PostgreSQL, которую будет использовать Django. |
| **POSTGRES_USER** | Имя пользователя PostgreSQL.|
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.|
| **POSTGRES_HOST** | Адрес сервера БД. В случае локальной разработки localhost.|
| **POSTGRES_PORT**  | Порт подключения к БД (по умолчанию `5432`). |
| **ALLOWED_HOSTS** | Хост(ы) для подключения |

### 3. Запуск PostgreSQL

Для работы приложения **TeamFinder** используется база данных **PostgreSQL**.
По условию задания база данных должна запускаться в контейнере Docker.

В проекте уже есть пример файла `docker-compose.yml`. Запустите контейнер:

```bash
docker compose up -d
```

### 4. Миграции базы данных

После запуска PostgreSQL примените миграции:

```bash
python manage.py migrate
```

### 5. Создание суперпользователя (администратора)
Для доступа в административную панель создайте суперпользователя:

```bash
python manage.py createsuperuser
```
Будут запрошены email, имя, фамилия, телефон (можно указать +70000000000) и пароль.

### 6. Создание демо-данныех (если нужны)
```bash
python manage.py seed_demo
```

После этого будет доступен пользователь:

```
email: maria@yandex.ru
password: password
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

Теперь проект доступен по адресу [http://localhost:8000/](http://localhost:8000). 

- Переход в админ-часть: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Главная страница: [http://localhost:8000/projects/list/](http://localhost:8000/projects/list/)
- Пользователи: [http://localhost:8000/users/list/](http://localhost:8000/users/list/), http://localhost:8000/users/<id>/
- Регистрация и вход: [http://localhost:8000/users/register/](http://localhost:8000/users/register/), [http://localhost:8000/users/login/](http://localhost:8000/users/login/)
- Управление проектами: [http://localhost:8000/projects/create-project/](http://localhost:8000/projects/create-project/), http://localhost:8000/projects/<id>/
- Автодополнение навыков: /projects/skills/?q=...
- Добавление/удаление навыков: /projects/<id>/skills/add/, /projects/<id>/skills/<skill_id>/remove/

---

## Технологический стек
| Наименование | Предназначение |
| - | - |
| Python 3.13 | основной язык разработки |
| Django 5.2 | веб-фреймворк для бэкенда |
| PostgreSQL | реляционная база данных (запускается в Docker-контейнере) |
| Docker & Docker Compose | контейнеризация базы данных (и опционально всего приложения). |
| Psycopg2‑binary | адаптер для подключения Django к PostgreSQL. |
| python-decouple | управление переменными окружения (файл .env). |
| Pillow | генерация аватарок (создание изображений с буквами, поддержка загрузки пользовательских фото). |
| HTML / CSS | шаблоны из статики.|
| JavaScript | для автодополнения навыков и отправки запросов на добавление/удаление навыков без перезагрузки страницы.|

---

Проект создан Семеновой Валерией в рамках обучения на курсах от "Бэкенд-разработчик на Django" от Яндекс Практикум
Контакты: [Почта](mailto:stw.vsemenova@yandex.ru)
