# Описание проделанной работы Задача #68: Написать APIView для новых пользователей

## Модель приложения “Custom_user” дополнена.
> confirmed_form_about_platform = models.BooleanField()
в связи с тем что необходимо проверять, отправляли мы письмо или нет

## Изменения:

> accounts / models / custom_user.py
- [x] Добавлена новая переменная которая отвечает за письма.

> accounts / ulrs.py
- [x] добавлен путь path("email/", views.EmailAPIView.as_view(), name="email").

> accounts / views.py
- [x] Функция send_email_survey_about_the_platform() с отправкой опроса на почту пользователя.
- [x] API класс EmailAPIView.

> settings / celery.py 
- [x] Внесены данные для работы Celery.

> settings / mail.py
- [x] Измененны переменные для правильности работы smtp и mail.

> requirements.txt
- [x] Был добавлен Celery в зависимости.


## Дополнительная информация для .env
>MAIL_SETTINGS_PORT = 465

>MAIL_SETTINGS_SERVER = 'smtp.yandex.ru' или другой stmp сервис.

>MAIL_SETTINGS_EMAIL_ADDRESS = 'YOUR@MAIL'

>MAIL_SETTINGS_EMAIL_PASSWORD = 'YOURPASSWORD'

>MAIL_SETTINGS_EMAIL_TIMEOUT = 60

>EMAIL_USE_TLS = False

>EMAIL_USE_SSL = True

>EMAIL_HOST_USER = MAIL_SETTINGS_EMAIL_ADDRESS

>EMAIL_HOST = MAIL_SETTINGS_SERVER