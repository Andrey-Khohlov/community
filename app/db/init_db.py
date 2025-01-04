from app.db.models import Base
from app.db.sessions import engine


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"DB has been initiated>": True}