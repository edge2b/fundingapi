# -*- coding: utf-8 -*-

import asyncio
import uvloop
import logging

import aioethereum
import asynctnt
from attrdict import AttrDict
from fundingapi.workers.handlers.check_balance import schedule_balance_checker

logger = logging.getLogger(__name__)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def periodical(env: AttrDict, fn: callable, period: int):
    while env.loop.is_running():
        # TODO: handler error
        await fn(env)
        await asyncio.sleep(period)


async def configure(env: AttrDict):
    env.tnt = asynctnt.Connection(host=env.cfg['tnt']['ip'], port=env.cfg['tnt']['port'])
    await env.tnt.connect()
    env.provider = {
        name: await aioethereum.create_ethereum_client(url, timeout=10)
        for (name, url) in env.cfg['provider'].items()
    }
    asyncio.ensure_future(periodical(env, schedule_balance_checker, 30))  # TODO: configure
