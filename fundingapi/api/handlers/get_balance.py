# -*- coding: utf-8 -*-
from aiohttp import web

from fundingapi.utils import generate_key_pair
from fundingapi.utils import is_address_valid

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

    result = await env.tnt.call('register_client', [api_key, address, inst['private'], inst['address']])
    if not result.body:
        return web.json_response({'error': 'Not valid or not active API Key'}, status=400)

    result = result.body[0]

    return web.json_response({'id': result['uuid'], 'address': inst['address']})
