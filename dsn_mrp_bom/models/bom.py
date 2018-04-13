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
import openerp.addons.decimal_precision as dp

class dsnMrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def _prepare_consume_line(self, bom_line, quantity, factor=1):
        result = super(dsnMrpBom,self)._prepare_consume_line(bom_line, quantity, factor)

        result.append({'priority': bom_line.sequence})

        return result

    dsn_pnt_nf = fields.Char(string="PNT NF", related="product_tmpl_id.dsn_pnt_nf", readonly=True)

class dsnMrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    product_qty= fields.Float(digits=dp.get_precision('Bom Line Qty'))
