import aiohttp
from aiohttp import web


async def get() -> web.Response:
    return aiohttp.web.Response(
        body=None,
        status=200,
    )
