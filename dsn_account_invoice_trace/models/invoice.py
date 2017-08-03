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

class dsnAccountInvoiceTrace(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_picking_ids(self):
        for record in self:
            if record.id:
                sale_obj = self.env['sale.order']
    #            op_obj = self.env['stock.pack.operation']
                sale_lst = sale_obj.search([('invoice_ids', '=',
                                             record.id)])
                record.dsn_picking_ids = sale_lst.mapped('picking_ids')
    #            op_lst = op_obj.search([('product_id', '=', self.product_id.id),
    #                                    ('picking_id', 'in',
    #                                     pickings.ids)])

    dsn_picking_ids = fields.Many2many(comodel_name='stock.picking',
                                        relation='dsn_invoice_picking',
                                        column1='invoice_id',
                                        column2='picking_id',
                                        string='Invoice Pickings',
                                        compute='_get_picking_ids',
                                        store=True)