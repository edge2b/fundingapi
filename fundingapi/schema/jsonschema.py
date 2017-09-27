# flake8: noqa
from collections import OrderedDict

jsonschema = OrderedDict([('createPairResponse',
              OrderedDict([('type', 'object'),
                           ('required', ['address', 'id']),
                           ('properties',
                            OrderedDict([('address',
                                          OrderedDict([('type', 'string'),
                                                       ('pattern',
                                                        '^0x[0-9abcdefABCDEF]{40}$'),
                                                       ('description',
                                                        'Etherium address'),
                                                       ('example',
                                                        1290543220439608419236362735313920956514209515868)])),
                                         ('id',
                                          OrderedDict([('type', 'string'),
                                                       ('format', 'uuid'),
                                                       ('description',
                                                        'Pair ID'),
                                                       ('example',
                                                        'd4171a66-af9f-493b-a4d7-dec0fc0c9e85')]))]))]))])
