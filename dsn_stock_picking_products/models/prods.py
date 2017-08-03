# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP SA (<http://openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class dsnStockPickingProduct(models.Model):
    _name='dsn.stock.picking.product'

    @api.multi
    @api.depends('picking_id.move_lines.product_id, picking_id.move_lines.product_qty')
    def _compute_products(self):
        for record in self:
            for prod in record.mapped('picking_id.move_lines.product_id'):
                _qty = 0
                for line in record.picking_id.move_lines.filtered(lambda x: x.product_id == prod):
                    _qty += line.product_qty

                record.product_id = prod
                record.qty = _qty

    picking_id = fields.Many2one(comodel_name='stock.picking')

    product_id = fields.Many2one(string='Product',
                                 comodel_name='product.product',
                                 compute='_compute_products',
                                 store=True)

    qty = fields.Float(string='Quantity',
                       compute='_compute_products',
                       digits=dp.get_precision('Product UoS'),
                       store=True)




class dsnStockPickingProds(models.Model):
    _inherit = 'stock.picking'

    dsn_product_ids = fields.One2many(comodel_name='dsn.stock.picking.product',
                                  inverse_name='picking_id',
                                  string='Picking Products')