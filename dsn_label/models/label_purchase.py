# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api
from openerp import tools
import datetime

class dsn_label_purchase (models.Model):
    _name = "dsn.label.purchase"
    _auto = False
    _description = "Invoice products"


    id = fields.Integer(string='id', readonly=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice', readonly=True)
#    pv = fields.Float(string="PV", readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    name = fields.Char(string='Description', readonly=True)
    price_unit = fields.Float(string='Price', readonly=True)
    discount = fields.Float(string='Discount', readonly=True)
    qua_valued = fields.Float(string='Quantity', readonly=True)
    qua_gift = fields.Float(string='Gift', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', readonly=True)

    def init(self, cr):

        tools.drop_view_if_exists(cr, 'dsn_account_invoice_product')
        cr.execute("""
            CREATE OR REPLACE VIEW dsn_account_invoice_product AS (
                select l.invoice_id as id, l.invoice_id as invoice_id, l.product_id, max(l.name) as name,
                max(price_unit) as price_unit,
                max(discount) as discount,
                sum(case price_unit when 0 then 0 else quantity end) as qua_valued,
                sum(case price_unit when 0 then quantity else 0 end) as qua_gift,
                sum(price_subtotal) as price_subtotal
                from account_invoice_line as l inner join account_invoice as o on
                o.id=l.invoice_id left join dsn_account_invoice_pv as opv on
                opv.invoice_id=l.invoice_id
                group by l.invoice_id, l.product_id
            )""")