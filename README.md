# Space_for_your_stories

Space_for_your_stories —  это проект социальной сети, где пользователи могут публиковать свои истории, делиться отзывами и общаться друг с другом. Проект покрыт Unit-тестами.

Функциональность проекта:
- регистрация и создание учетных записей;
- публикация постов и комментариев;
- подписка на авторов;
- редактирование и удаление постов и комментариев;
- просмотр информации о постах и комментариях для неавторизованных пользователей.

### Технологии
[![Django](https://img.shields.io/badge/Django-4.2.1-blue?logo=django)](https://www.djangoproject.com/)
[![Django](https://img.shields.io/badge/pytest--django-4.4.0-blue?logo=Django)](https://pypi.org/project/pytest-django/)


### Запуск проекта:
Клонировать репозиторий:
```
git clone https://github.com/Tatiana314/Space_for_your_stories.git && cd Space_for_your_stories
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
python -m venv venv
Linux/macOS: source env/bin/activate
windows: source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
В директории Space_for_your_stories создать и заполнить файл .env:
```
touch .env

SECRET_KEY='Секретный ключ'
ALLOWED_HOSTS='Имя или IP хоста'
DEBUG=True
```
Выполнить миграции и запустить проект:
```
python manage.py migrate && python manage.py runserver
```
После запуска, проект доступен по адресу: http://127.0.0.1:8000/.

- http://127.0.0.1:8000/admin/ - панель администратора;

- http://127.0.0.1:8000/about/author/ - информация об авторе проекта;
- http://127.0.0.1:8000/about/tech/ - информация о технологиях проекта;

- http://127.0.0.1:8000/auth/signup/ - регистрация пользователя;
- http://127.0.0.1:8000/auth/logout/ - разлогирование пользователя,
- http://127.0.0.1:8000/auth/login/ - авторизирование пользователя,
- http://127.0.0.1:8000/auth/password_change/ - смена пароля пользователем;
- http://127.0.0.1:8000/auth/password_reset/ - восстановление пароля пользователем;

- http://127.0.0.1:8000/ - главная страница, отображение всех опубликованных постов;
- http://127.0.0.1:8000/group/{slug}/ - отображение постов относящихся к определенной группе;
- http://127.0.0.1:8000/profile/{username}/ - страница автора;
- http://127.0.0.1:8000/posts/{post_id}/ - страница с постом;
- http://127.0.0.1:8000/posts/{post_id}/edit/ - страница поста, с формой для редактирования;
- http://127.0.0.1:8000/posts/{post_id}/comment/ - все комментарии определенного поста;
- http://127.0.0.1:8000/follow/ - посты всех авторов, на которых подписан пользователь;
http://127.0.0.1:8000/profile/{username}/follow/ - подписка пользователя на автора;
http://127.0.0.1:8000/profile/{username}/unfollow/ - отписка пользователя от автора;

## Автор
[Мусатова Татьяна](https://github.com/Tatiana314)
