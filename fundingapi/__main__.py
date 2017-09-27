#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import click
import yaml

from .commands import api_group
# from commands.workers import workers_group

logger = logging.getLogger(__name__)


@click.command(cls=click.CommandCollection, sources=[api_group])  # type: ignore
@click.option('--debug', is_flag=True, default=False)
@click.option('--config',
              type=click.Path(readable=True, exists=True, dir_okay=False, resolve_path=True),
              default="config.yaml",
              required=True)
@click.pass_context
def cli(ctx: click.core.Context, debug: bool, config: str) -> None:
    ctx.obj['cfg'] = yaml.load(open(config).read())
    ctx.obj['debug'] = debug
    format = '%(asctime)s [%(name)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format=format)


if __name__ == '__main__':
    cli(obj={})
