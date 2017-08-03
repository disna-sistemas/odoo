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

class dsnStockPickingExport(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends('origin')
    def _compute_sale_order(self):
        for record in self:


            sale_order_model = record.env['sale.order']
            _origin=record.origin
            _origin=_origin.replace(chr(47),'_').replace(chr(92),'_')
            cond = [('name', '=', _origin)]
            sale_orders = sale_order_model.search(cond)
            if sale_orders:
                record.dsn_sale_order = sale_orders[0]
#                for sale_order in sale_orders:
#                    record.dsn_sale_order = sale_order

    dsn_sale_order = fields.Many2one(comodel_name='sale.order',
                                     string='Sale Order',
                                     compute='_compute_sale_order',
                                     store=True)