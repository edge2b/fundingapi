# -*- coding: utf-8 -*-
import asyncio
import logging

import click
from attrdict import AttrDict
from ..api import route


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
