from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine)

from sqlalchemy import URL
import os

url = URL.create(
    drivername='postgresql+asyncpg',
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    host=os.environ['DB_HOST'],
    port=int(os.environ['DB_PORT']),
    database=os.environ['DB_NAME']
    )

_engine = create_async_engine(
    url=url,
    pool_size=40,
    max_overflow=80)

get_async_session = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=_engine)