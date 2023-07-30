# fastapi_menus

## Описание
REST API по работе с меню ресторана в качестве домашнего задания на интенсиве YLab_University


## Как запустить проект:

## 1. В контейнер

###  _Если у вас не установлены Docker и Docker-compose необходимо воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/)._

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Maliarda/fastapi_menus.git
```
```
cd fastapi_menus
```

### Заполните .docker.env необходимыми данными или оставьте без изменения

### Для запуска проекта используйте команду:

```
docker-compose -f docker-compose.yml up --build
```

### Документация будет доступна по адресу:

[http://localhost:8000/docs](http://localhost:8000/docs)

### Для запуска тестов используй команду:

```
docker-compose -f docker-compose-test.yml up --build
```

### Остановить контейнеры можно командой:
```
docker-compose stop
```

## 2. Локально
### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Maliarda/fastapi_menus.git
```
```
cd fastapi_menus
```

### Создать базу данных основную и для тестов:
Возможно с помощью [PGAdmin](https://info-comp.ru/install-pgadmin-4-on-windows-10#nastroyka-podklyucheniya-k-postgresql) или DBeaver


### В корневом каталоге проекта создать файл с именем .env, в который добавить следующие переменные (см. example_env):

> DATABASE_URL=postgresql+asyncpg://user:password@host:port/db_name
> POSTGRES_URL_TEST=postgresql+asyncpg://user:password@host:port/test_db_name

#### где: 
- user:password - данные для подключения к базе данных, 
- host:port - имя и порт сервера базы данных, 
- dbname - название базы данных,
- test_db_name - название базы данных для тестов

### Создать и активировать виртуальное окружение:

Команда для установки виртуального окружения на Mac или Linux:
```
python3 -m venv env
source env/bin/activate
```
Команда для Windows должна быть такая:
```
python -m venv venv
source venv/Scripts/activate
```
### Обновить pip:

```
python -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
alembic upgrade head
```

### Запустить проект:

```
uvicorn app.main:app 
```
### Запустить тесты можно командой:

```
python -m pytest -v
```

### Документация доступна по адресам:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
