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
from datetime import datetime
import logging

class dsnSaleOrderTotals(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends('order_line.price_unit','order_line.product_uos_qty')
    def _compute_promo(self):
        _logger = logging.getLogger(__name__)
        for record in self:
            _before = datetime.now()
            _promoqty = 0
            for line in record.order_line.filtered(lambda x: x.price_unit == 0):

#                if line.price_unit == 0:
                _promoqty += line.product_uos_qty
            record.dsn_promo_qty = _promoqty

            _after = datetime.now()

            diff_in_secs = (_after - _before).total_seconds()
            _logger.info('sale order ' + record.name + ' seconds computing promo : ' + str(diff_in_secs))

    dsn_promo_qty = fields.Float("Promo Quantity",
                          compute='_compute_promo',
                          store=True)