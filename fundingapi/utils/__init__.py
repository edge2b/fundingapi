import binascii
import re

import sha3
from ecdsa import SECP256k1
from ecdsa import SigningKey
from fundingapi import const
from web3 import Web3


def generate_key_pair():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak.update(pub)
    address = keccak.hexdigest()[24:]

    return {
        'private': '0x{}'.format(binascii.b2a_hex(priv.to_string()).decode()),
        'pub': '0x{}'.format(binascii.b2a_hex(pub).decode()),
        'address': Web3.toChecksumAddress('0x{}'.format(address))
    }


def hex2skey(hx):
    return SigningKey.from_string(
        binascii.a2b_hex(hx[2:]),
        curve=SECP256k1
    )

is_address_valid = re.compile(const.ETHEREUM_ADDRESS_RE).match
