from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from cfhqd.config import settings

engine = create_async_engine(settings.db_uri, echo=True)

session = AsyncSession(bind=engine)

