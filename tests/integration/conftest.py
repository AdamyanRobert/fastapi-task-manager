import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport

from main import app
from src.database import Base
from src.dependencies import get_db_session


@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer("postgres:15") as pg:
        yield pg


@pytest_asyncio.fixture(scope="function")
async def async_engine(postgres_container):
    url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    engine = create_async_engine(url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db(async_engine):
    """Создаём таблицы перед тестом и очищаем после."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_integration_client(async_engine):
    async def get_test_db():
        async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_test_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
