from aiohttp.test_utils import AioHTTPTestCase

from attrdict import AttrDict
from fundingapi.api.route import make_app
from fundingapi.schema import createPairResponse
from hypothesis import given

from .strategies import ST_ETHEREUM_ADDRESS


class ConfigTestCase(AioHTTPTestCase):

    async def get_application(self):
        env = AttrDict()
        return make_app(env)


class TestConfig(ConfigTestCase):
    @given(ethereum_address=ST_ETHEREUM_ADDRESS)
    def test_valid(self, ethereum_address):
        async def go():
            response = await self.client.get('/api/create_pair/{}'.format(ethereum_address.strip()))
            assert response.status == 200
            body = await response.json()
            createPairResponse(body)
        self.loop.run_until_complete(go())
