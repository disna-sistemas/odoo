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

class dsnMrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    @api.depends('move_lines.product_id')
    def _compute_lotsemi(self):
        for mline in self.move_lines.filtered(lambda x: x.product_id.dsncat2_id.name in ('SEMI','SE')):
            lot_obj = self.env['stock.production.lot']
            lot_lst = lot_obj.search([('name','=','L0221A')])
            for l in lot_lst:
                mline.dsn_lotsemi = l
                break

#            for quant in mline.reserved_quant_ids:
#                mline.dsn_lotsemi = quant.lot_id

    dsn_lotsemi = fields.Many2one(comodel_name='stock.production.lot',
                                  string='Lote Semi',
                                  compute='_compute_lotsemi',
                                  store=True)