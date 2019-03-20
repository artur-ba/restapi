import logging
import typing

from aiohttp import web
import asyncpg
import ujson

from service.models import user

LOG = logging.getLogger(__name__)


async def _get_user(user_id: str, db_pool: asyncpg.pool.Pool) -> typing.Dict[str, typing.Any]:
    async with db_pool.acquire() as conn:
        database_user = await conn.fetchrow('SELECT * FROM users WHERE id = $1', user_id)
        if not database_user:
            raise web.HTTPNotFound(body=ujson.dumps({'message': 'User does not exist'}))
        return database_user


async def get(user_id: str, db_pool: asyncpg.pool.Pool) -> web.Response:
    LOG.info('Received request to get user by id')
    single_user = await _get_user(user_id, db_pool)
    return web.json_response(
        data=user.User(
            id=str(single_user['id']),
            userName=single_user['user_name'],
            firstName=single_user['first_name'],
            lastName=single_user['last_name'],
            email=single_user['email'],
            address=single_user['address'],
            postalCode=single_user['postal_code'],
        ),
        dumps=user.User.dumps,
    )


async def delete(user_id: str, db_pool: asyncpg.pool.Pool) -> web.Response:
    LOG.info('Received request to delete user')
    await _get_user(user_id, db_pool)
    async with db_pool.acquire() as conn:
        try:
            await conn.execute('DELETE FROM users WHERE id = $1', user_id)
        except asyncpg.PostgresError:
            LOG.exception('Failed to delete user')
            raise web.HTTPInternalServerError(body=ujson.dumps({'message': 'Failed to delete user'}))
    return web.json_response(
        data='',
        status=204,
    )
