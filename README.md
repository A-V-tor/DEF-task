## Задание: Написать парсер для странички https://web.samokat.ru

Основные моменты:
- Для главной странички и одной (любой) категории написать парсер, который соберет информацию по нескольким продуктам (можно ограничить 10-15, важно не сколько, а как);
- Данные можно сохранять как угодно, идеал - postgres;
- Развернуть можно как угодно, идеал - dосker, который можно будет запустить локально;
- Код выложить куда угодно;
Каких-то других принципиальных моментов нет.
<hr>
<h1 align="center">Развертывание проекта</h1>

Скачать проект

```
  git clone git@github.com:A-V-tor/DEF-task.git
```

```
  cd dismantling-samokat
```

Запустить сборку докер-compose
```
docker-compose up
```
### Подождать запуск всех контейнеров и дать скрипту поработать 5 минут, для сбора данных. </br> </br>
<img src="https://github.com/A-V-tor/DEF-task/blob/main/screen-log.png">

### Для удобства по адрессу http://127.0.0.1:5000/admin/ развернута админ панель для работы с моделями базы данных. </br> </br>
<img src="https://github.com/A-V-tor/DEF-task/blob/main/screen-admin.png">

## Пароль для подключения через PG-ADMIN: admin
