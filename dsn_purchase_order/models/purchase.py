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

class dsnPurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _order = "date_order desc, name"

class dsnPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
#    _order = "date_planned desc, name"
    _order = "id"

class dsnPurchasereport(models.Model):
    _inherit = "purchase.report"

    dsncat2_id = fields.Many2one(comodel_name='product.category',
                                 string='Cat2',
                                 related='product_id.dsncat2_id',
                                 readonly=True,
                                 store=True)

