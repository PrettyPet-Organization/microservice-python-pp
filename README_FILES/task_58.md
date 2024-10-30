# Задача 58 - Настроить админку

## Основные задачи:
* насторить админку для моделей проекта
* определить какие поля выводить
* добавить display_venue для определнных моделей
* настроить фильтр 
* и т.д.
## Основные параметры

- **list_display**: поля, отображаемые в списке пользователей.
- **list_editable**: поля, которые можно редактировать прямо из списка.
- **readonly_fields**: поля, которые нельзя редактировать в админке.
- **search_fields**: поля, по которым доступен поиск.
- **list_filter**: фильтры для удобного поиска пользователей.
- **fieldsets**: структура формы редактирования пользователя.

## Комментарии 
  `Так как нужно заполнить бд что бы видеть как отображаются данные, наткнулся на некоторые проблемы. Поэтому залез в модели и дописал что то в них.
  Если отменить все изменения в моделях то ничего не сломается, будет просто не так эстетично отображаться некоторые данные в админ панели.`

## `src/core/admin.py`

- Настроены основные заголовки и метаданные для административной панели проекта:
  - **site_title**: "Pretty Pet admin (DEV)" — заголовок вкладки админ-панели.
  - **site_header**: "Pretty Pet administration" — заголовок страницы администрирования.
  - **index_title**: "Site administration" — заголовок главной страницы панели администрирования.

## `src/accounts/admin.py`

- **AdminCustomUser**: Интерфейс администрирования для модели `CustomUser`.
    - Поля для отображения (`list_display`): `username`, `email`, `phone_number`, `date_joined`, `is_superuser`, `is_active`, `is_staff`.
    - Редактируемые поля (`list_editable`): `is_superuser`, `is_active`, `is_staff`.
    - Поля только для чтения (`readonly_fields`): `date_joined`, `last_login`.
    - Поля для поиска (`search_fields`): `username`, `email`, `phone_number`.
    - Фильтры (`list_filter`): `is_active`, `is_staff`, `is_superuser`.
    - Группы полей (`fieldsets`):
        - Раздел "Permissions & Status": `is_superuser`, `groups`, `user_permissions`, `is_staff`, `is_active`.
        - Раздел "User Info": `username`, `email`, `phone_number`.
        - Раздел "Important Dates": `date_joined`, `last_login` (скрытый по умолчанию).

## `src\common\models\news.py`
- Добавлена мета информация для корректного отображения множественного числа "News"

## `src\common\models\topics.py`
- Добавлен дандер метод __str__ для корректного отображения в панели "Topic № - topic_name" 

## `src/common/admin.py`

- **AdminNews**: Интерфейс администрирования для модели `News`.
    - Поля для отображения (`list_display`): `title`, `author_info`, `is_open`, `likes`, `topics_list`, `tags_list`, `image_url`.
    - Редактируемые поля (`list_editable`): `is_open`.
    - Поля для поиска (`search_fields`): `title`, `description`, `author`.
    - Фильтры (`list_filter`): `is_open`, `topics`, `author`, `tags`.
    - Поля только для чтения (`readonly_fields`): `likes`.
    - Группы полей (`fieldsets`):
        - Основной раздел: `title`, `description`, `image_url`, `author`, `likes`, `is_open`.
        - Раздел "Relations": `topics`, `tags`.

- **AdminRoles**: Интерфейс администрирования для модели `Role`.
    - Поля для отображения (`list_display`): `role_name`.
    - Поля для поиска (`search_fields`): `role_name`.

- **AdminTags**: Интерфейс администрирования для модели `Tag`.
    - Поля для отображения (`list_display`): `tag_name`.
    - Поля для поиска (`search_fields`): `tag_name`.

- **AdminTools**: Интерфейс администрирования для модели `Tool`.
    - Поля для отображения (`list_display`): `tool_name`.
    - Поля для поиска (`search_fields`): `tool_name`.

- **AdminTopic**: Интерфейс администрирования для модели `Topic`.
    - Поля для отображения (`list_display`): `topic_name`.
    - Поля для поиска (`search_fields`): `topic_name`.

- **AdminUsefulMaterials**: Интерфейс администрирования для модели `UsefulMaterial`.
    - Поля для отображения (`list_display`): `title`, `description`, `image_url`, `likes`, `link_name`.
    - Поля для поиска (`search_fields`): `title`, `link_name`.
    - Фильтры (`list_filter`): `likes`.

## `src\hackathons\models\hackathon_prizes.py`
  - Изменён дандер __str__ метод для корректоного отображения связаного с призом хакатона. Было: "hackathons.Hackathon.None | Name"
  - Добавлена мета информация для корректного отображения множественного числа "Hackathon prizes"

## `src/hackathons/admin.py`
- **HackathonNameMixin**: Миксин для отображения названий хакатонов в моделях админки.
    - метод `hackathon_name()`: Возвращает название связанного хакатона.

- **AdminHackaton**: Интерфейс администрирования для модели `Hackathon`.
    - Поля для отображения (`list_display`): `hackathon`, `type`, `name`, `core_idea`, `task`, `start_date`, `finish_date`, `image_url`, `prize_name`.
    - Только для чтения (`readonly_fields`): `hackathon`, `start_date`.
    - Поля для поиска (`search_fields`): `name`, `core_idea`, `task`.
    - Фильтры (`list_filter`): `type`, `start_date`, `finish_date`.
    - Группировка полей (`fieldsets`): Общая информация, Даты, Медиа, Призы и связи.

- **AdminGroupsInHackathon**: Интерфейс для управления моделью `GroupsInHackathon`.
    - Поля для отображения: `group`, `hackathon`.
    - Поля для поиска: `group`, `hackathon`.
    - Фильтры: `hackathon`.

- **AdminGroupsForHackathon**: Интерфейс для управления моделью `GroupsForHackathon`.
    - Поля для отображения: `group`, `group_name`.
    - Поля для поиска: `group`, `group_name`.
    - Фильтры: `group`.

- **AdminParticipantsInHackathon**: Интерфейс для управления моделью `ParticipantsInHackathon`, использует `HackathonNameMixin`.
    - Поля для отображения: `participant`, `hackathon_name`, `profile`.
    - Поля для поиска: `hackathon_name`, `profile`.
    - Фильтры: `hackathon`, `profile`.

- **AdminHackathonPrizes**: Интерфейс для управления моделью `HackathonPrizes`.
    - Поля для отображения: `hackathon_name`, `name`, `description`, `image_url`.
    - Поля для поиска: `name`.

- **AdminRolesInHackathon**: Интерфейс для управления моделью `RolesInHackathon`, использует `HackathonNameMixin`.
    - Поля для отображения: `hackathon_name`, `role_name`, `participants_needed`.
    - Фильтры: `role`, `participants_needed`.

- **AdminTagsInHackathon**: Интерфейс для управления моделью `TagsInHackathon`, использует `HackathonNameMixin`.
    - Поля для отображения: `hackathon_name`, `tag_name`.
    - Поля для поиска: `tag`.
    - Фильтры: `tag`.

- **AdminToolsInHackathon**: Интерфейс для управления моделью `ToolsInHackathon`, использует `HackathonNameMixin`.
    - Поля для отображения: `hackathon_name`, `tool_name`, `participants_needed`.
    - Поля для поиска: `tool`, `participants_needed`.
    - Фильтры: `tool`, `participants_needed`.

## `src\profiles\models\cities.py`
  - Добавлена мета информация для корректного отображения множественного числа "Cities"

## `src/profiles/admin.py`

- **AdminProfile**: Интерфейс администрирования для модели `Profile`.
    - Поля для отображения (`list_display`): `user`, `public_name`, `age`, `city_name`, `photo_url`.
    - Поля для поиска (`search_fields`): `user__username`, `public_name`, `city`.
    - Фильтры (`list_filter`): `city`, `age`.
    - Только для чтения (`readonly_fields`): `photo_url`.
    - Функция `city_name()`: Возвращает название города, связанного с профилем.

- **AdminCity**: Интерфейс администрирования для модели `City`.
    - Поля для отображения (`list_display`): `name`, `slug`.
    - Поля для поиска (`search_fields`): `name`, `slug`.

## `src/projects/admin.py`

- **ProjectNameMixin**: Миксин для отображения названия проекта в моделях админки.
    - метод `project_name()`: Возвращает название связанного проекта.

- **FinishedStatusFilter**: Пользовательский фильтр для модели `Project`, позволяющий фильтровать проекты по статусу завершенности (`finished` или `not_finished`).

- **AdminProject**: Интерфейс администрирования для модели `Project`.
    - Поля для отображения (`list_display`): `project_name`, `core_idea`, `status`, `finish_date`, `is_finished`, `tool_name`, `role_name`, `tag_name`.
    - Поля для поиска (`search_fields`): `project_name`, `core_idea`, `description`.
    - Фильтры (`list_filter`): `FinishedStatusFilter`, `status`, `project_type`, `tags`, `groups`.
    - Только для чтения (`readonly_fields`): `is_finished`.

- **AdminProjectTypes**: Интерфейс администрирования для модели `ProjectType`.
    - Поля для отображения (`list_display`): `type_name`.
    - Поля для поиска (`search_fields`): `type_name`.

- **AdminRolesInProject**: Интерфейс администрирования для модели `RolesInProject`.
    - Поля для отображения (`list_display`): `role_name`, `project_name`, `participants_needed`.
    - Поля для поиска (`search_fields`): `role`, `project`.
    - Фильтры (`list_filter`): `role`, `project`, `participants_needed`.
    - Функция `role_name()`: Возвращает название роли.

- **AdminToolsInProject**: Интерфейс администрирования для модели `ToolsInProject`.
    - Поля для отображения (`list_display`): `tool_name`, `project_name`, `participants_needed`.
    - Поля для поиска (`search_fields`): `tool`, `project`.
    - Фильтры (`list_filter`): `tool`, `project`, `participants_needed`.
    - Функция `tool_name()`: Возвращает название инструмента.
