import logging, asyncio

from attrdict import AttrDict
from functools import partial
from web3 import HTTPProvider
from web3 import Web3

logger = logging.getLogger(__name__)


async def process_mapping(env: AttrDict, mapping: dict):
    network_name = mapping['resource']['network_type']
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
        #  buyTokens(address contributor) -> 0xec8ac4d8 + uint256 address
        'data': '0xec8ac4d8{0:064x}'.format(int(mapping['client_address'], 16)),
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

