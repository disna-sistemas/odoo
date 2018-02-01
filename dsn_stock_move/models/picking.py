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
from datetime import datetime

class dsnStockMove(models.Model):
    _inherit = "stock.move"
#    _order = "date desc, name"

    @api.multi
    @api.depends('product_id')
    def _compute_customer_product_name(self):
        for record in self:
            record.dsn_customer_product_name=record.product_id.product_tmpl_id.customer_ids.filtered(lambda x: x.name.id==record.picking_id.partner_id.id)

    dsn_customer_product_name = fields.Char(string='Partner-Product Name',
                                           compute='_compute_partner_product_name',
                                            store=True)

class dsnProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"


    @api.multi
    @api.onchange('product_name')
    def dsn_update_move_lines_partner_product_name(self):
        res = {}
        for record in self:
            if record.type == 'customer':
                move_ids = self.env['stock.move'].search([('state','!=','done'),('product_id.product_tmpl_id','=',record.product_id.product_tmpl_id)])
                for move_id in move_ids:
                    move_id.dsn_customer_product_name = record.product_name
        return res