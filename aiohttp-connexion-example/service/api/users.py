import logging
import typing
import uuid

from aiohttp import web
import asyncpg
import ujson

from service.models import user

LOG = logging.getLogger(__name__)


async def get(db_pool: asyncpg.pool.Pool, last_name: typing.Optional[str] = None) -> web.Response:
    LOG.info('Received request to list users')
    query = 'SELECT * FROM users'
    if last_name:
        query = f'{query} WHERE last_name LIKE %{last_name}%;'
    users = []
    async with db_pool.acquire() as conn:
        async with conn.transaction():
            async for u in conn.cursor(query):
                users.append(
                    user.User(
                        id=str(u['id']),
                        userName=u['user_name'],
                        firstName=u['first_name'],
                        lastName=u['last_name'],
                        email=u['email'],
                        address=u['address'],
                        postalCode=u['postal_code'],
                    ),
                )
    return web.json_response(data=users, dumps=user.User.dumps)


async def post(body: typing.Dict[str, typing.Any], db_pool: asyncpg.pool.Pool) -> web.Response:
    LOG.info('Received request to create new user')
    user_id = str(uuid.uuid4())
    async with db_pool.acquire() as conn:
        try:
            database_user = await conn.fetchrow('SELECT id FROM users WHERE user_name = $1 ', body['user_name'])
            if database_user:
                raise web.HTTPConflict(body=ujson.dumps({'message': 'User already exists'}))
            await conn.execute(
                'INSERT INTO users(id, user_name, first_name, last_name, email, address, postal_code)'
                'VALUES ($1, $2, $3, $4, $5, $6, $7)',
                user_id,
                body['user_name'],
                body['first_name'],
                body['last_name'],
                body['email'],
                body.get('address', ''),
                body.get('postal_code', ''),
            )
        except asyncpg.PostgresError:
            LOG.exception('Failed to add user')
            raise web.HTTPInternalServerError(body=ujson.dumps({'message': 'Failed to create new user'}))
    return web.json_response(
        data=user.User(
            id=user_id,
            userName=body['user_name'],
            firstName=body['first_name'],
            lastName=body['last_name'],
            email=body['email'],
            address=body.get('address'),
            postalCode=body.get('postal_code'),
        ),
        dumps=user.User.dumps,
    )
