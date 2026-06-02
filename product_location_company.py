# This file is part product_warehouse_position module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import Eval, If
from trytond.transaction import Transaction


class ProductPosition(metaclass=PoolMeta):
    __name__ = 'product.position'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.warehouse.domain = [
            *cls.warehouse.domain,
            ('company',
                If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ]

    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False,
            query=False):
        company_id = Transaction().context.get('company')
        operator = '=' if company_id else '!='
        domain = [domain, [('warehouse.company', operator, company_id or -1)]]
        return super().search(domain, offset=offset, limit=limit, order=order,
            count=count, query=query)

    @classmethod
    def read(cls, ids, fields_names=None):
        ids = [p.id for p in cls.search([('id', 'in', ids)])]
        if not ids:
            return []
        return super().read(ids, fields_names=fields_names)


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.positions.domain = [
            ('warehouse.company',
                If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ]
