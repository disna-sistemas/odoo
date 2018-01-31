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

from openerp import models, fields, api, _, exceptions

class dsnStockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.multi
    @api.depends('quant_ids')
    def _compute_lots(self):
        if self.quant_ids:
            for record in self:
                if record.quant_ids:
                    record.dsn_lot_ids = record.quant_ids.mapped('lot_id')

    dsn_lot_ids = fields.One2many(comodel_name='stock.production.lot',
                                    relation='dsn_package_lot_rel',
                                    column1='package_id',
                                    column2='lot_id',
                                    string='Lots',
                                    compute='_compute_lots',
                                    store=True)