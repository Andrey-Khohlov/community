- запуск контейнеров 

<code>
docker compose up
</code>

- запуск базы 

<code>
source .venv/bin/activate
</code>

- проверка базы

<code>
$ docker exec -it my-postgres psql -U postgres

postgres=# SELECT * FROM users;
</code>

- запуск бэкэнда

<code>
fastapi dev app/main.py

uvicorn app.main:app --reload
</code>

- запуск фронтэнда

<code>
python3 -m frontend.pages.login

flet run --web --port 8002 frontend/login.py
</code>

- запуск приложения

<code>
docker compose up
</code>

- если падает с ошибкой переноса контекста:

<code>
sudo chown -R $USER:$USER /home/xgb/PycharmProjects/coffee_chat/db
</code>

- подключиться к базе:

<code>
docker compose exec db /bin/bash
 
psql -U postgres -d postgres
</code>

\d users

- проверить и убить процессы

<code>
sudo lsof -i :8550

sudo kill -9 <PID>
</code>

- для создания дампа:

<code>
docker exec <container_id> pg_dumpall -U <username> > backup_all.sql
</code>

- сжать логи

<code>
sudo journalctl --vacuum-size=100M 
</code>

- проверить Dos/DDoS атаки

<code>
tail -10000 /var/log/nginx/access.log | awk '{print $1}'| sort -nr | uniq -c | sort -nr | head

tail -10000 /var/log/nginx/unauthorized.access.log | awk '{print $1}'| sort -nr | uniq -c | sort -nr | head
</code>

# Alembic
alembic revision --autogenerate -m "Add new column"
alembic upgrade head