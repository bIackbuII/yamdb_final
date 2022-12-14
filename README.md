# Финальный проект «API для Yatube» ![example workflow](https://github.com/bIackbuII/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Описание
Проект полезен тем, что в первую очередь даёт возможность взаимодействовать с сайтом и пользоваться функционалом, не заходя на сайт. 
##### Функционал:
###### POSTS
- Получить список всех публикаций
- Создать новую публикацию
- Получить публикацию по id
- Обновить публикацию по id
- Частично обновить публикацию по id
- Удалить публикацию по id
###### COMMENTS
- Получить список всех комментариев публикации
- Создать новый комментарий для публикации
- Получить комментарий для публикации по id
- Частично обновить комментарий для публикации по id
- Удалить комментарий для публикации по id
###### AUTH
- Получить JWT-токен
- Обновить JWT-токен
###### FOLLOW
- Получить список всех подписчиков для пользователя, отправившего запрос
- Создать подписку
###### GROUP
- Получить список всех групп
- Создать новую группу

Документация к API доступна по адресу `http://127.0.0.1/redoc/`
## Установка
#### 1. Клонируем репозиторий на локальную машину:

- `git clone https://github.com/bIackbuII/infra_sp2.git`

#### 2. Запускаем Docker

#### 3. Открываем терминал на локальной машине

#### 4. Переходим в директорию `infra` склонированного репозитория

#### 5. Выполняем команду для сборки и запуска контейнеров:

- `docker-compose up -d`

#### 6. Переходим в консоль контейнера с веб-приложением (дальнейшие команды будут применятся из консоли контейнера)

- `docker exec -it <CONTAINER_ID> bash`

#### 7. Выполняем миграции:

- `python manage.py migrate`

#### 8. Создаем суперпользователя:

- `python manage.py createsuperuser`

#### 9. Создаем резервную копию базы данных

- `python manage.py dumpdata > fixtures.json`

## Адрес для ознакомления с работой приложения

https://chernovol.ddns.net/
