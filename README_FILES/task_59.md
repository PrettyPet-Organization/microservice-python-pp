# Задача 59 - Русификация админки

- [x] Админ панель была переведена на Русский язык.
- [x] Была сделана локализация в locale для ru
- [x] Добавлены/измененны в i18n (settings) следующие строки
- LANGUAGE_CODE = "ru"
- TIME_ZONE = "Europe/Moscow"
- USE_I18N = True
- USE_L10N = True
- USE_TZ = True
- LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

Для работы с русификацией необходимо из раздела src ввести данную команду
python manage.py compilemessages   