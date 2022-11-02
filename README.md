# API YaMDb
## _Проект для обмена данными с сервисом YaMDb через API_
## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
Запросы к API начинаются с
```sh
/api/v1/
```
## Установка:
1. Клонируйте репозиторий, перейдите в него:
```sh
git clone git@github.com:Rendlolx/api_yamdb.git
cd api_yamdb
```
2. Создайте и активируйте виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
```
3. Установите зависимости:
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Перейдите в папку api_yamdb, выполните миграции, запустите проект:
```sh
cd api_yamdb
python manage.py migrate
python manage.py runserver
```
## Примеры:
### Алгоритм регистрации пользователей:
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле.
Передавайте в Headers-Authorization: токен для запросов к API, например:
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ (GET, POST, PUT, PATCH, DELETE)
```
для работы с отзывами
Более подробно с возможностями API можно ознакомиться в документации по адресу: 
```sh
http://127.0.0.1:8000/redoc/
```
после запуска проекта.
