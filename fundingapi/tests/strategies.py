import hypothesis.strategies as st
from fundingapi import const
from hypothesis_regex import regex

ST_ETHEREUM_ADDRESS = regex(const.ETHEREUM_ADDRESS_RE)
ST_TIMESTAMP = st.integers(0, 2**32 - 1)
