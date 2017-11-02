import logging, asyncio

from attrdict import AttrDict
from functools import partial
from web3 import HTTPProvider
from web3 import Web3

logger = logging.getLogger(__name__)


async def process_mapping(env: AttrDict, mapping: dict):
    network_name = mapping['resource']['network_name']
    provider = env.provider[network_name]
    endpoint = env.cfg['provider'][network_name]
    balance = await provider.eth_getBalance(mapping['funding_address'])
    w3 = Web3([HTTPProvider(endpoint)])

    if balance < 1e17:  # TODO: config
        logger.debug(f"Process mapping {mapping['uuid']}, not enough ETH ({balance/1e18}) on {mapping['funding_address']}")
        await env.tnt.call('update_recheck', [mapping['uuid'], 30])
        return

    gas = 90000  # TODO: config
    gas_price = 20e9  # TODO: config

    if network_name == 'ropsten':
        chain_id = 3
    elif network_name == 'rinkeby':
        chain_id = 4
    elif network_name == 'kovan':
        chain_id = 42
    else:
        chain_id = 1

    transaction = {
        'to': mapping['resource']['contract_address'],
        'from': mapping['funding_address'],
        'value': balance - gas * gas_price,
        'gas': gas,
        'gasPrice': gas_price,
        'data': '0xec8ac4d8000000000000000000000000{0:040x}'.format(int(mapping['client_address'], 16)),
        'chainId': chain_id,
        'nonce': 0,
    }
    signed = w3.eth.account.signTransaction(transaction, mapping['private_key'])
    tx_id = await provider.eth_sendRawTransaction(signed.rawTransaction.hex())
    await env.tnt.call('assign_tx_id', [mapping['uuid'], tx_id])
    logger.debug(f"Process mapping {mapping['uuid']}, send {transaction['value']/1e18} ETH to contract {transaction['to']} -> {tx_id}")


async def schedule_balance_checker(env: AttrDict):
    mappings = (await env.tnt.call('get_mappings')).body[0]
    logger.info(f"Process mappings — check balance changes (found {len(mappings)})")
    if len(mappings) == 0:
        return
    await asyncio.wait(map(partial(process_mapping, env), mappings))


# from json import loads, dumps

# import aiohttp

# from attrdict import AttrDict
# from fundingapi.utils import hex2skey
# im
# from web3 import HTTPProvider
# from web3 import Web3

# async def rpc_call(endpoint: str, method: str, params: list, id: int):
#         data = {
#             'jsonrpc': '2.0',
#             'method': method,
#             'params': params,
#             'id': id,
#         }
#         with aiohttp.ClientSession() as session:
#             r = yield from session.post(
#                 url=endpoint,
#                 data=dumps(data),
#                 headers={'Content-Type': 'application/json'}
#             )
#         response = yield from r.json(loads=json.loads)



# async def schedule_balance_checker(env: AttrDict):
#     infura_provider = HTTPProvider('https://ropsten.infura.io')
#     w3 = Web3([infura_provider])
#     mappings = (await env.tnt.call('get_mappings')).body[0]
#     for mapping in mappings:
#         skey = hex2skey(mapping['private_key'])
#         transaction = {
#             'to': mapping['resource']['contract_address'],
#             'value': 1000000000,
#             'gas': 2000000,
#             'gasPrice': 234567897654321,
#             'nonce': 0,
#             'chainId': 1
#         }
#         # w3.eth.account.signTransaction()
# #         >>> transaction = {
# #         'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
# #         'value': 1000000000,
# #         'gas': 2000000,
# #         'gasPrice': 234567897654321,
# #         'nonce': 0,
# #         'chainId': 1
# #     }
# # >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
# # >>> signed = w3.eth.account.signTransaction(transaction, key)
# # {'hash': HexBytes('0x6893a6ee8df79b0f5d64a180cd1ef35d030f3e296a5361cf04d02ce720d32ec5'),
# #  'r': HexBytes('0x09ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9c'),
# #  'rawTransaction': HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),
# #  's': HexBytes('0x440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),
# #  'v': 37}
# # >>> w3.eth.sendRawTransaction(signed.rawTransaction)
# #         print(skey)
#         print(mapping)
#     import ipdb
#     ipdb.set_trace()
#     pass
