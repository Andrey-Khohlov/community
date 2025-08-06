## Запуск
- запуск контейнеров
```
docker compose up
```

- запуск базы
```
source .venv/bin/activate
```
- запуск бэкэнда

```
fastapi dev app/main.py
uvicorn app.main:app --reload
```

- запуск фронтэнда

```
python3 -m frontend.pages.login
flet run --web --port 8002 frontend/login.py
```

- запуск приложения

```
docker compose up
```
- если не билдится, проверить и убить процессы

```
sudo lsof -i :8550
sudo kill -9 <PID>
```
- активация виртуальной среды
```commandline
source .venv/bin/activate
```
## База данных
- проверка базы

```
$ docker exec -it my-postgres psql -U postgres
postgres=# SELECT * FROM users;
```
- если падает с ошибкой переноса контекста:
```
sudo chown -R $USER:$USER /home/xgb/PycharmProjects/coffee_chat/db
```

- подключиться к базе:

```
docker compose exec db /bin/bash
psql -U postgres -d postgres
\d users
```


- для создания дампа:

```
docker exec <container_id> pg_dumpall -U <username> > backup_all.sql
```

## Место на диске
- сжать логи

```
sudo journalctl --vacuum-size=100M 
```


## Рутинные проверки
- проверить Dos/DDoS атаки

```
tail -10000 /var/log/nginx/access.log | awk '{print $1}'| sort -nr | uniq -c | sort -nr | head
tail -10000 /var/log/nginx/unauthorized.access.log | awk '{print $1}'| sort -nr | uniq -c | sort -nr | head
```
- сертификаты HTTPS
```
sudo certbot certificates
xgb@xgb-MS-7788:~$ cat /etc/crontab  # из директории к которой применяллся крон, здесь: xgb@xgb-MS-7788:~$ 
sudo /opt/certbot/bin/pip install --upgrade certbot certbot-nginx  # ежемесячно
```
- восстановлеие базы из резервной копии на google
- восстановлеие базы из резервной копии на диске
## Alembic
```
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## Nginx
``` 
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
sudo nano /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl restart nginx
sudo tail -f /var/log/nginx/error.log
```
логи `/var/log/nginx`
## Fierwall
```
sudo ufw allow 443/tcp
```

