запуск базы 

<code>
$ docker exec -it my-postgres psql -U postgres
postgres=# SELECT * FROM users;
</code>

запуск приложения

<code>
fastapi dev app/main.py
uvicorn app.main:app --reload

</code>