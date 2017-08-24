schema_add = {'product_id': {'type': 'string', 'empty': False,
                             'required': True},
              'quality': {'type': 'integer', 'empty': False,
                          'required': True}}

schema_order = {'email': {'type': 'string', 'empty': False, 'required': True},
                'phone': {'type': 'string', 'empty': False, 'required': True},
                'name':  {'type': 'string', 'empty': False, 'required': True},
                'address':
                {'type': 'dict',  'empty': False, 'required': True,
                                  'schema':
                                  {'line1': {'type': 'string', 'empty': False,
                                             'required': True},
                                   'city': {'type': 'string', 'empty': False,
                                            'required': True},
                                   'state': {'type': 'string'},
                                   'country': {'type': 'string'},
                                   'postal_code': {'type': 'string'}
                                   }
                 }
                }
