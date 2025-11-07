from trytond.pool import PoolMeta
from trytond.model import fields, ModelSQL, ModelView
from trytond.transaction import Transaction


class ProductPosition(ModelSQL, ModelView):
    'Product Position'
    __name__ = 'product.position'

    template = fields.Many2One('product.template', 'Product Template',
        required=True)
    warehouse = fields.Many2One('stock.location', 'Warehouse', required=True,
        domain=[('type', '=', 'warehouse')])
    position = fields.Char('Position')

    @classmethod
    def default_warehouse(cls):
        return Transaction().context.get('warehouse')


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    positions = fields.One2Many('product.position', 'template',
        'Positions')
