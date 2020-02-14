# Журнал входящих дел (v.19)

## Скриншот
![screenshot here](/screenshots/screenshot_sm.png)

## Использование (Flask в docker контейнере)

### Сборка docker image
```sh
$ docker build -t flask-exp19 .
```

### Запуск контейнера
Необходимо передать переменные окружения `MYSQL_EXP_USER`, `MYSQL_EXP_PASS`, `MYSQL_EXP_HOST`. Это можно сделать через файл `env.list`, содержащий строки вида `VAR=VAL`. Например:

```
# EXP-FLASK credentials
MYSQL_EXP_USER=xxxxxxxx
MYSQL_EXP_PASS=xxxxxxxx
MYSQL_EXP_HOST=xxx.xxx.xxx.xxx
```

```sh
$ docker run -d --name flask-exp -p 10050:80 -v $(pwd)/app:/app --env-file ~/env.list flask-exp19
```

## TODOs
 - Add Tests
 - Add database create scripts