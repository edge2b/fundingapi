# -*- coding: utf-8 -*-
import logging
import os

import yaml
from attrdict import AttrDict

from .api import route

logger = logging.getLogger(__name__)


def main():
    config = os.environ.get('CFG') or 'server/config.yaml'
    env = AttrDict()
    env.cfg = yaml.load(open(config).read())
    return route.make_app(env)


app = main()
