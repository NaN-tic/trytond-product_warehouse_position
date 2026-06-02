# This file is part product_warehouse_position module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.modules.company.tests import CompanyTestMixin, create_company
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import with_transaction
from trytond.transaction import Transaction


class ProductLocationLinkTestCase(CompanyTestMixin, ModuleTestCase):
    'Test Product Location Link module'
    module = 'product_warehouse_position'
    extras = ['stock_location_company']

    @with_transaction()
    def test_positions_current_company(self):
        pool = Pool()
        Location = pool.get('stock.location')
        ProductPosition = pool.get('product.position')
        Template = pool.get('product.template')
        Uom = pool.get('product.uom')

        kilogram, = Uom.search([
                ('name', '=', 'Kilogram'),
                ], limit=1)
        template, = Template.create([{
                    'name': 'Test Product',
                    'type': 'goods',
                    'default_uom': kilogram.id,
                    'products': [('create', [{}])],
                    }])

        company1 = create_company()
        company2 = create_company('Michael Scott Paper Company',
            currency=company1.currency)
        company2.save()

        warehouse1 = self.create_warehouse(Location, company1, '1')
        warehouse2 = self.create_warehouse(Location, company2, '2')

        position1, position2 = ProductPosition.create([{
                    'template': template.id,
                    'warehouse': warehouse1.id,
                    'position': 'A1',
                    }, {
                    'template': template.id,
                    'warehouse': warehouse2.id,
                    'position': 'B1',
                    }])

        with Transaction().set_context(
                company=company1.id,
                companies=[company1.id, company2.id]):
            positions = ProductPosition.search([
                    ('template', '=', template.id),
                    ])
            self.assertEqual(positions, [position1])
            self.assertEqual(
                ProductPosition.read([position1.id, position2.id], ['position']),
                [{'id': position1.id, 'position': 'A1'}])

        with Transaction().set_context(
                company=company2.id,
                companies=[company1.id, company2.id]):
            positions = ProductPosition.search([
                    ('template', '=', template.id),
                    ])
            self.assertEqual(positions, [position2])
            self.assertEqual(
                ProductPosition.read([position1.id, position2.id], ['position']),
                [{'id': position2.id, 'position': 'B1'}])

    @staticmethod
    def create_warehouse(Location, company, suffix):
        with Transaction().set_context({
                    'company': company.id,
                    'companies': [company.id],
                    }):
            storage = Location(
                name='Storage %s' % suffix,
                type='storage',
                code='STO%s' % suffix,
                )
            storage.save()
            warehouse = Location(
                name='Warehouse %s' % suffix,
                code='WH%s' % suffix,
                type='warehouse',
                company=company,
                input_location=storage,
                output_location=storage,
                storage_location=storage)
            warehouse.save()
            return warehouse

del ModuleTestCase
