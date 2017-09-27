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
    # import ipdb
    # ipdb.set_trace()
    # schema['title'] = 'Class'
    # builder = pjs.ObjectBuilder(schema)
    # ns = builder.build_classes(strict=True)
    # if 'properties' in schema:
    #     ns.Class.__keys__ = schema['properties'].keys()
    # globals()[name] = ns.Class


def validate(schema: abc.ABC) -> callable:
    def wrap(fn: callable) -> callable:
        async def decor(request: web.Request) -> web.Response:
            text = await request.text()
            try:
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    raise pjs.validators.ValidationError('Wrong json format')
                if isinstance(data, dict):
                    inst = schema(**data)
                    inst.validate()
                else:
                    raise pjs.validators.ValidationError('Wrong data structure, should be a dict')
            except pjs.validators.ValidationError as e:
                return web.json_response({'error': str(e)}, status=400)
            return await fn(inst.as_dict())
        return decor
    return wrap
