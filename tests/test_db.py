import asyncio
import asyncpg

async def test_connection():
    try:
        # Подключение к базе данных
        conn = await asyncpg.connect(
            user="postgres",       # Пользователь
            password="relfhtim",   # Пароль
            database="postgres", # Имя базы данных
            host="db",       # Хост (имя сервиса в Docker)
            port=5432              # Порт
        )
        print("✅ Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Запуск асинхронной функции
asyncio.run(test_connection())