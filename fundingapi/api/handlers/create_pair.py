# -*- coding: utf-8 -*-
import re
import uuid

from aiohttp import web

from fundingapi import const
from fundingapi.utils import generate_key_pair

is_address_valid = re.compile(const.ETHEREUM_ADDRESS_RE).match
# from ...schema import updateRequest
# from ...schema import validate


# @validate(updateRequest)
async def handler(data):
    address = data.match_info['address']
    if not is_address_valid(address):
        return web.json_response({'error': 'Not valid address'}, status=400)
    inst = generate_key_pair()
    return web.json_response({'address': inst['address'], 'id': str(uuid.uuid4())})
