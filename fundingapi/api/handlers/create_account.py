# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from fundingapi.utils import generate_key_pair
from fundingapi.utils import is_address_valid

from ...schema import registerRequest
from ...schema import validate

logger = logging.getLogger(__name__)


@validate(registerRequest)
async def handler(request, data):
    env = request.app['env']
    address = data['address']
    email = data['email'].lower()
    name = data['name']
    api_key = request.headers.get('X-API-KEY')

    if not api_key:
        return web.json_response({'error': 'Need API Key'}, status=400)

    if not is_address_valid(address):
        return web.json_response({'error': 'Not valid address'}, status=400)

    payload = [api_key, address, email, name]
    result = await env.tnt.call('create_account', payload)
    print(result)
    if not result.body:
        return web.json_response({'error': 'Not valid or not active API Key'}, status=400)

    result = result.body[0]
    logger.info(f"Create account {address}/{email} for {api_key}")
    return web.json_response({'id': result['uuid'], 'contract': result['resource']})
