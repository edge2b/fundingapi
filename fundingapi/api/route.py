# -*- coding: utf-8 -*-

import logging

from aiohttp import web

import asynctnt
from attrdict import AttrDict

from .handlers import handler_create_account
from .handlers import handler_create_pair

logger = logging.getLogger(__name__)


def make_app(env: AttrDict) -> web.Application:
    app = web.Application()
    app['env'] = env
    app.router.add_route('POST', '/api/create_pair', handler_create_pair)
    app.router.add_route('POST', '/api/create_account', handler_create_account)
    return app


async def configure(env: AttrDict):
    handler = make_app(env).make_handler()
    env.tnt = asynctnt.Connection(host=env.cfg['tnt']['ip'], port=env.cfg['tnt']['port'])
    await env.tnt.connect()
    srv = await env.loop.create_server(handler, env.cfg['http']['ip'], env.cfg['http']['port'])

    return srv, handler
