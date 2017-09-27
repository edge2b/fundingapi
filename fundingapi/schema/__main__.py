#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
from collections import OrderedDict
from pprint import pformat

import click

import jsonref
import yaml
from yaml import Loader

logger = logging.getLogger(__name__)
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


Loader.add_constructor(_mapping_tag, dict_constructor)


@click.command()  # type: ignore
@click.option('--source',
              type=click.Path(readable=True, exists=True, dir_okay=False, resolve_path=True),
              required=True)
@click.option('--destination',
              type=click.Path(dir_okay=False, resolve_path=True),
              required=True)
def cli(source: str=None, destination: str=None) -> None:
    raw = open(source).read()
    inst = yaml.load(raw, Loader=Loader)
    inst = jsonref.loads(json.dumps(inst), object_pairs_hook=OrderedDict)
    open(destination, 'w').write(
        '# flake8: noqa\n'
        'from collections import OrderedDict\n'
        '\n'
        'jsonschema = {}\n'.format(pformat(inst['definitions']))

    )


if __name__ == '__main__':
    cli()
