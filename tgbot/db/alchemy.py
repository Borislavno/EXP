from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tgbot import config


Base = declarative_base()
Session = sessionmaker(expire_on_commit=False, class_=AsyncSession)


# Documentation
# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
async def setup_db():
    engine = create_async_engine(config.POSTGRES_URI, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # Documentation
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html
    Session.configure(bind=engine)
