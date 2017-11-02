from aiohttp.test_utils import AioHTTPTestCase

from attrdict import AttrDict
from fundingapi.api.route import make_app
from fundingapi.schema import createPairResponse
from hypothesis import given

from .strategies import ST_ETHEREUM_ADDRESS
from .strategies import ST_TIMESTAMP


class ConfigTestCase(AioHTTPTestCase):

    async def get_application(self):
        env = AttrDict()
        return make_app(env)


class TestConfig(ConfigTestCase):
    @given(
        address=ST_ETHEREUM_ADDRESS,
        expired_at=ST_TIMESTAMP
    )
    def test_valid(self, **data):
        async def go():
            response = await self.client.post(
                '/api/create_pair',
                headers={'X-API-KEY': '19061f36-3f2b-408a-aaec-dcdcfb2c30be'},
                json=data
            )
            assert response.status == 200, await response.text()
            body = await response.json()
            createPairResponse(body)
        self.loop.run_until_complete(go())
