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
                                                        'Ethereum address'),
                                                       ('example',
                                                        '0xe20df59ecc01ee28e3e794d64f37c6961bae495c')])),
                                         ('id',
                                          OrderedDict([('type', 'string'),
                                                       ('format', 'uuid'),
                                                       ('description',
                                                        'Pair ID'),
                                                       ('example',
                                                        'd4171a66-af9f-493b-a4d7-dec0fc0c9e85')]))]))])),
             ('createPairRequest',
              OrderedDict([('type', 'object'),
                           ('required', ['address']),
                           ('properties',
                            OrderedDict([('address',
                                          OrderedDict([('type', 'string'),
                                                       ('pattern',
                                                        '^0x[0-9abcdefABCDEF]{40}$'),
                                                       ('description',
                                                        'Ethereum address'),
                                                       ('example',
                                                        '0xe20df59ecc01ee28e3e794d64f37c6961bae495c')]))]))])),
             ('registerRequest',
              OrderedDict([('type', 'object'),
                           ('required', ['name', 'email', 'address']),
                           ('properties',
                            OrderedDict([('address',
                                          OrderedDict([('type', 'string'),
                                                       ('pattern',
                                                        '^0x[0-9abcdefABCDEF]{40}$'),
                                                       ('description',
                                                        'Ethereum address'),
                                                       ('example',
                                                        '0xe20df59ecc01ee28e3e794d64f37c6961bae495c')])),
                                         ('email',
                                          OrderedDict([('type', 'string'),
                                                       ('format', 'email'),
                                                       ('description',
                                                        'User mail'),
                                                       ('example',
                                                        'me@daedalus.ru')])),
                                         ('name',
                                          OrderedDict([('type', 'string'),
                                                       ('pattern',
                                                        '^(.+){4,}$'),
                                                       ('description',
                                                        'User Fullname'),
                                                       ('example',
                                                        'Nick Smith')]))]))])),
             ('registerResponse',
              OrderedDict([('type', 'object'),
                           ('required', ['id']),
                           ('properties',
                            OrderedDict([('id',
                                          OrderedDict([('type', 'string'),
                                                       ('format', 'uuid'),
                                                       ('description',
                                                        'Pair ID'),
                                                       ('example',
                                                        'd4171a66-af9f-493b-a4d7-dec0fc0c9e85')]))]))]))])
