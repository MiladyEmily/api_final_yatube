#YaTUBE API

### Описание проекта yatube_api

Yatube - это социальная сеть для публикации своих мыслей (желательно котов). Этот репозиторий - API проекта Yatube.

При помощи Yatube API можно:
* 🐈 создавать свои записи по группам или без них (только про котов)
* 🐈 прикреплять к постам картинки (конечно же котов!)
* 🐈 просматривать группы и все посты в них (боооольше котов)
* 🐈 просмотривать и комментировать записи других пользователей (писать, насколько великолепны их мохнатыши)
* 🐈 подписываться на пользователей (которые постят самых красивых котиков)

Проект создан, чтобы отработать навыки работы с Django REST API Framework.

### Технологии:

Python 3.7 | Django 3.2.16 | Django REST Framework 3.12.4 | Simple JWT 4.7.2


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MiladyEmily/api_final_yatube
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
