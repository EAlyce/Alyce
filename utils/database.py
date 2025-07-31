"""
Alyce 框架数据库支持（异步SQLAlchemy，默认SQLite）
插件可直接 import get_db_session()
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ.get("ALYCE_DB_URL", "sqlite+aiosqlite:///alyce.db")
engine = create_async_engine(DB_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
