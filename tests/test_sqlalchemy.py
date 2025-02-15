from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

async def test_sqlalchemy_connection():
    DATABASE_URL = "postgresql+asyncpg://postgres:relfhtim@db:5432/postgres"
    engine = create_async_engine(DATABASE_URL, echo=True)

    try:
        # Проверка подключения
        async with engine.connect() as conn:
            print("✅ Connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        await engine.dispose()

# Запуск асинхронной функции
asyncio.run(test_sqlalchemy_connection())