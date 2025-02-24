import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import  FastAPI

import uvicorn

from app.api.v1.endpoints import coffees, users, reviews, comments
from app.db.init_db import setup_database, insert_init_data


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Жизненный цикл приложения."""
#     # print("Setting up the database...")
#     # res = await setup_database()  # Выполняем настройку базы данных
#     # print(*list(res.keys()))
#     #  - TODO убрать после тестов - На проде не используем!
#     # 'print("Inserting initial data...")'
#     # 'res = await insert_init_data() or {'No data to insert': None}'
#     # 'print(*list(res.keys()))'
#     yield  # Продолжаем запуск приложения
#     print("Application shutdown.")

app = FastAPI()  #lifespan=lifespan)

# Подключаем роутеры
app.include_router(coffees.router, prefix="/v1/coffees", tags=["coffees"])
app.include_router(users.router, prefix="/v1/users", tags=["users"])
app.include_router(reviews.router, prefix="/v1/reviews", tags=["reviews"])
app.include_router(comments.router, prefix="/v1", tags=["comments"])


if __name__ == "__main__":
    if os.getenv("DOCKER_ENV") == "true":
        uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run('main:app',  reload=True)