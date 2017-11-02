import abc
import json

from aiohttp import web

# import python_jsonschema_objects as pjs
import trafaret as t
from trafaret_schema import json_schema, Register, just

try:
    from .jsonschema import jsonschema
except ImportError:
    jsonschema = dict({})


register = Register()
check_uuid = t.OnError(t.Regexp('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), 'Not valid UUID')
register.reg_format('uuid', just(check_uuid))


for (name, schema) in jsonschema.items():
    rule = json_schema(dict(schema), context=register)
    globals()[name] = rule


def validate(schema: abc.ABC) -> callable:
    def wrap(fn: callable) -> callable:
        async def decor(request: web.Request) -> web.Response:
            text = await request.text()
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return web.json_response({'error': 'Wrong json format'}, status=400)

            if isinstance(data, dict):
                try:
                    data = schema(data)
                except t.dataerror.DataError as e:
                    return web.json_response({'error': e.error[0].as_dict()}, status=400)
            return await fn(request, data)
        return decor
    return wrap
