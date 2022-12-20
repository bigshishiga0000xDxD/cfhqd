import asyncio

from cfhqd.db.connection import engine
from cfhqd.db.tables import Base


async def main():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

if __name__ == '__main__':
    asyncio.run(main())
