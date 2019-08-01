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

    @api.multi
    @api.depends('product_id')
    def _compute_category_levels(self):
        for record in self:
            record.dsncat1_id = record.product_id.dsncat1_id
            record.dsncat2_id = record.product_id.dsncat2_id
            record.dsncat3_id = record.product_id.dsncat3_id
            record.dsncat4_id = record.product_id.dsncat4_id
            record.dsncat5_id = record.product_id.dsncat5_id

    @api.multi
    @api.depends('product_id')
    def _compute_partner_product_name(self):
        for record in self.filtered(lambda mv: not mv.picking_id is None):
            for prod_custom_info in record.product_id.product_tmpl_id.customer_ids.filtered(
                lambda x: x.name.id == record.picking_id.partner_id.id):
                if prod_custom_info.name:
                    record.dsn_customer_product_name = prod_custom_info.product_name

    dsn_customer_product_name = fields.Char(string='Partner-Product Name',
                                            compute='_compute_partner_product_name',
                                            store=True)


    dsncat1_id = fields.Many2one('product.category',
                                 string='Cat1',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

    dsncat2_id = fields.Many2one('product.category',
                                 string='Cat2',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

    dsncat3_id = fields.Many2one('product.category',
                                 string='Cat3',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

    dsncat4_id = fields.Many2one('product.category',
                                 string='Cat4',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

    dsncat5_id = fields.Many2one('product.category',
                                 string='Cat5',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

