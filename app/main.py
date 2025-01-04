import asyncio
from fastapi import  FastAPI

import uvicorn

from app.api.v1.endpoints import coffees
from app.db.init_db import setup_database



app = FastAPI()

# Подключаем роутеры
app.include_router(coffees.router, prefix="/v1/coffees", tags=["coffees"])

setup_database()


if __name__ == "__main__":
    # uvicorn.run('main:app', host="0.0.0.0", port=80, reload=True)
    uvicorn.run('main:app',  reload=True)