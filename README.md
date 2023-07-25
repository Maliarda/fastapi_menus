# fastapi_menus

## Описание
REST API по работе с меню ресторана в качестве домашнего задания на интенсиве YLab_University


## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Maliarda/fastapi_menus.git
```
```
cd fastapi_menus
```

### Создать базу:
Возможно с помощью [PGAdmin](https://info-comp.ru/install-pgadmin-4-on-windows-10#nastroyka-podklyucheniya-k-postgresql) или DBeaver


### В корневом каталоге проекта создать файл с именем .env, в который добавить следующие переменные:

> DATABASE_URL=postgresql+asyncpg://user:password@host:port/db_name

#### где: 
- user:password - данные для подключения к базе данных, 
- host:port - имя и порт сервера базы данных, 
- dbname - название базы данных.

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
