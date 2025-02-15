запуск базы 

<code>
source .venv/bin/activate
</code>

<code>
$ docker exec -it my-postgres psql -U postgres
postgres=# SELECT * FROM users;
</code>

запуск бэкэнда

<code>
fastapi dev app/main.py
uvicorn app.main:app --reload

</code>

запуск фронтэнда

<code>
flet run --web --port 8002 frontend/login.py
</code>

запуск приложения

<code>
docker compose up
</code>

если падает с ошибкой переноса контекста:

<code>
sudo chown -R $USER:$USER /home/xgb/PycharmProjects/coffee_chat/db
</code>

подключиться к базе:

<code>
docker-compose exec db /bin/bash
psql -U myuser -d mydatabase
psql -h db -U postgres -d postgres
</code>