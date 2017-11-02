# -*- coding: utf-8 -*-
import asyncio
import logging

import click
from attrdict import AttrDict
from fundingapi.api import route
from fundingapi.workers import configure as workers_configure


logger = logging.getLogger(__name__)


@click.group()
def api_group():
    pass


@api_group.command()
@click.option('--timeout', type=click.IntRange(1, 5000), default=1000, required=True)
@click.pass_context
def api(ctx, timeout):
    """API"""
    env = AttrDict()
    env.cfg = ctx.obj['cfg']
    loop = env.loop = asyncio.get_event_loop()
    env.loop.create_task(route.configure(env))
    loop.run_forever()


@click.group()
def workers_group():
    pass


@workers_group.command()
@click.option('--timeout', type=click.IntRange(1, 5000), default=1000, required=True)
@click.pass_context
def workers(ctx, timeout):
    """Workers"""
    env = AttrDict()
    env.cfg = ctx.obj['cfg']
    loop = env.loop = asyncio.get_event_loop()
    env.loop.create_task(workers_configure(env))
    loop.run_forever()
