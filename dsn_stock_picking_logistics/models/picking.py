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

class dsnStockPickingLogistics(models.Model):
    _inherit = "stock.picking"

    dsn_manual_weight = fields.Float(string='Manual Weight',
                        help="Gross weight",
                        digits=dp.get_precision('Stock Weight'))

    dsn_manual_volume = fields.Float(string='Manual Volume',
                                 help="Volume in m3",
                                 digits=dp.get_precision('Stock Volume'))



