from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)

from app.core.config import settings

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_psycopg,
#     echo=True,
# )
async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)
# session_factory = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        yield session
