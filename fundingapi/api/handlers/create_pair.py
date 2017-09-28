# -*- coding: utf-8 -*-
import re

from aiohttp import web

from fundingapi import const
from fundingapi.utils import generate_key_pair

is_address_valid = re.compile(const.ETHEREUM_ADDRESS_RE).match
# from ...schema import updateRequest
# from ...schema import validate


# @validate(updateRequest)
async def handler(data):
    env = data.app['env']
    address = data.match_info['address']
    api_key = data.headers.get('X-API-KEY')
    if not api_key:
        return web.json_response({'error': 'Need API Key'}, status=400)

    if not is_address_valid(address):
        return web.json_response({'error': 'Not valid address'}, status=400)

    inst = generate_key_pair()
    result = await env.tnt.call('register_client', [api_key, address, inst['private'], inst['address']])
    if not result.body:
        return web.json_response({'error': 'Not valid or not active API Key'}, status=400)

    result = result.body[0]

    return web.json_response({'id': result['uuid'], 'address': inst['address']})
