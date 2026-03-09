import os
from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Post(DeclarativeBase):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#it will create all tables from classes which inherits DeclarativeBase
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

#it is going to get a session which will allow us to actually use the DB and write & read from it asynchronously
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

