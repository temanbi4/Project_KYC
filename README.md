<h3 align="center">
Программа для отчётности и уведомления о загрузке, принятия или отклонения документов для администратора и авторизованных пользователей. </h3>

Микросервис позволяет отправлять письмо администратору о загрузке нового документа на сервис.
При подтверждении документа или отклонении его администратором, пользователю отправляется соответствующее уведомление.  
Проект использует celery для асинхронной отправки уведомлений, в качестве брокера используется redis.

Стек проекта: <br>
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) - 3.10<br>
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) - 5.0<br>
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) - 3.14.0<br>
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) - 16.1<br>
![Celery](https://img.shields.io/badge/celery-%2300C7B7.svg?style=for-the-badge&logo=celery&logoColor=white) - 5.3.6<br>
![Redis](https://img.shields.io/badge/redis-%23DC382D.svg?style=for-the-badge&logo=redis&logoColor=white) - 5.0.1<br>
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) - 24.0.7


**Перед запуском проекта** необходимо создать и заполнить свой файл .env своими данными по примеру из файла env.sample.<br>
А так же в файле docker-compose.yaml в параметрах запуска kyc_app_1 указать данные для авторизации Администратора.
#### ___Состав файла env.___

SECRET_KEY=<br>
DB_NAME=<br>
DB_USER=<br>
DB_PASSWORD=<br>
DB_HOST=kyc_db_1 (for docker)<br>
EMAIL_HOST_USER=<br>
EMAIL_HOST_PASSWORD=<br>
EMAIL_HOST=<br>
EMAIL_PORT=<br>

#### _Запуск в докер контейнере_

docker-compose up -d

#### Тесты
Покрытие 75% pytest <br>
Запуск тестов - coverage run --source='.' manage.py test <br>
Посмотреть покрытие - coverage report

#### Описание моделей

Модель Document: <br>
user - Указывает на пользователя, используя внешний ключ. <br>
file  - Поле для хранения файла документа. Файлы сохраняются в папке "documents/". <br>
uploaded_at  - Дата и время загрузки документа, устанавливается автоматически при создании. <br>
is_approved - Флаг, указывающий, подтвержден ли документ администратором. По умолчанию установлен в False. <br>
is_rejected - Флаг, указывающий, отклонен ли документ администратором. По умолчанию установлен в False. <br>
Модель User:  <br>
email - Уникальное поле для адреса электронной почты пользователя. <br>
telegram_id - Поле для хранения идентификатора пользователя в Telegram. Может быть пустым. <br>

#### Права доступа
Каждый авторизованный пользователь может видеть список только своих загруженных документов. <br>
Администратор может видеть список всех загруженных документов, а также имеет возможность подтверждать, отклонять или удалять их. <br>

#### Эндпоинты
Регистрация нового пользователя  <br>
POST запрос http://127.0.0.1:8080/register/  <br>
Получение данных профиля текущего пользователя  <br>
GET запрос http://127.0.0.1:8080/profile/  <br>
Получение токена доступа на основе учетных данных  <br>
POST запрос http://127.0.0.1:8080/token/  <br>
Обновление токена доступа с использованием токена обновления  <br>
POST запрос http://127.0.0.1:8080/token/refresh/ <br>
Создание нового документа <br>
POST запрос http://127.0.0.1:8080/create/ <br>
Получение списка всех документов <br>
GET запрос http://127.0.0.1:8080/list/ <br>
Получение, изменение и удаление деталей документа <br>
GET, PUT, DELETE запрос http://127.0.0.1:8080/detail/<int:pk>/ <br>

#### Документация проекта
http://127.0.0.1:8080/swagger/ или http://127.0.0.1:8080/redoc/

Проект выполнил Ершов Артем на IDE 
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
