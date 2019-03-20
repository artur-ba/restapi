import typing

import aiohttp
from aiohttp import web

AIO_HANDLER = typing.Callable[[web.Request], typing.Awaitable[web.Response]]
AIO_MIDDLEWARE = typing.Callable[[aiohttp.web.Request, AIO_HANDLER], typing.Coroutine[typing.Any, typing.Any, web.
                                                                                      Response]]


def get() -> typing.List[AIO_MIDDLEWARE]:
    return [init]


@web.middleware
async def init(
        request: web.Request,
        handler: AIO_HANDLER,
) -> web.Response:
    request['db_pool'] = request.app['db_pool']
    response = await handler(request)
    response.enable_compression()
    return response
