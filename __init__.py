# This file is part product_location_link module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.ProductLocationLink,
        product.Template,
        module='product_location_link', type_='model')
