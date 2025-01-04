import asyncio
from contextlib import asynccontextmanager

from fastapi import  FastAPI

import uvicorn

from app.api.v1.endpoints import coffees
from app.db.init_db import setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения."""
    print("Setting up the database...")
    res = await setup_database()  # Выполняем настройку базы данных
    print(*list(res.keys()))
    yield  # Продолжаем запуск приложения
    print("Application shutdown.")

app = FastAPI(lifespan=lifespan)

# Подключаем роутеры
app.include_router(coffees.router, prefix="/v1/coffees", tags=["coffees"])

# res = asyncio.run(setup_database())
# print(res)
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(setup_database())
# print(result)

if __name__ == "__main__":
    # uvicorn.run('main:app', host="0.0.0.0", port=80, reload=True)
    uvicorn.run('main:app',  reload=True)