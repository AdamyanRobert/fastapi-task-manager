from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_engine = create_async_engine(
    echo=True,
    url=settings.DATABASE_URL_asyncpg,

)

session_sync = sessionmaker(sync_engine)
session_async = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
