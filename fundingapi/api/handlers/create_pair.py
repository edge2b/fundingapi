# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from fundingapi.utils import generate_key_pair
from fundingapi.utils import is_address_valid

from ...schema import createPairRequest
from ...schema import validate

logger = logging.getLogger(__name__)


@validate(createPairRequest)
async def handler(request, data):
    env = request.app['env']
    address = data['address']
    expired_at = data['expired_at']
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return web.json_response({'error': 'Need API Key'}, status=400)

    if not is_address_valid(address):
        return web.json_response({'error': 'Not valid address'}, status=400)

    inst = generate_key_pair()
    payload = [api_key, address, inst['private'], inst['address'], int(expired_at)]
    result = await env.tnt.call('register_client', payload)
    if not result.body:
        return web.json_response({'error': 'Not valid or not active API Key'}, status=400)

    result = result.body[0]
    logger.info(f"Register mapping {address} -> {inst['address']} for {api_key}")
    return web.json_response({'id': result['uuid'], 'address': inst['address']})
