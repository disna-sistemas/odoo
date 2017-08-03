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

from openerp import models, fields

class product(models.Model):
    _inherit = "product.product"


#    dsn_box_barcode = fields.Char(string='Box Barcode', help='GTIN 14')
#    dsn_box_config = fields.Char(string='Box Config', help='Ex: 12 x 300 ml')
#    dsn_box_units = fields.Integer(string='Box Units', help='Number of units per box')

    dsn_calc_cost = fields.Boolean(string="Calculate cost", default=True)
