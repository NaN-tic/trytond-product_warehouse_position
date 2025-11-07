from trytond.pool import PoolMeta
from trytond.model import fields, ModelSQL, ModelView
from trytond.transaction import Transaction


class ProductLocationLink(ModelSQL, ModelView):
    'Product Location Link'
    __name__ = 'product.location.link'

    template = fields.Many2One('product.template', 'Product Template',
        required=True)
    warehouse = fields.Many2One('stock.location', 'Warehouse', required=True,
        domain=[('type', '=', 'warehouse')])
    location = fields.Char('Location')

    @classmethod
    def default_warehouse(cls):
        return Transaction().context.get('warehouse')


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    location_links = fields.One2Many('product.location.link', 'template',
        'Locations')
