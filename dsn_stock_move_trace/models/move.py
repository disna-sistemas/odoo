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

class dsnStockMoveTrace(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _get_production_ids(self):
        for record in self.filtered(lambda x: x.location_dest_id.usage=='production'):
            if record.id:
                prod_obj = self.env['mrp.production']
                prod_lst = prod_obj.search([('invoice_ids', '=',
                                             record.id)])
                record.dsn_picking_ids = prod_lst.mapped('picking_ids')
    #            op_lst = op_obj.search([('product_id', '=', self.product_id.id),
    #                                    ('picking_id', 'in',
    #                                     pickings.ids)])

    dsn_production_ids = fields.Many2many(comodel_name='mrp.production',
                                        relation='dsn_move_production',
                                        column1='production_id',
                                        column2='move_id',
                                        string='Invoice Pickings',
                                        compute='_get_picking_ids',
                                        store=True)