import os
import typing

from aiohttp import web
import asyncpg


async def get_db_engine(app: web.Application) -> typing.AsyncIterator[None]:
    app['db_pool'] = await asyncpg.create_pool(
        # connect args
        user='postgres',
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database='users',
        host='localhost',
        port=5432,
    )

    yield

    await app['db_pool'].close()
