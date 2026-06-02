# This file is part product_warehouse_position module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import product_location_company

def register():
    Pool.register(
        product.ProductPosition,
        product.Template,
        module='product_warehouse_position', type_='model')
    Pool.register(
        product_location_company.ProductPosition,
        product_location_company.Template,
        module='product_warehouse_position', type_='model',
        depends=['stock_location_company'])
