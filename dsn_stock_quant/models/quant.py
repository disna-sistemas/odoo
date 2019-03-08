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
import openerp.addons.decimal_precision as dp

class dsnStockQuant(models.Model):
    _inherit = "stock.quant"

    @api.multi
    @api.depends('location_id')
    def _compute_location_levels(self):
        for record in self:
            record.dsnloc1_id = record.location_id.dsnloc1_id
            record.dsnloc2_id = record.location_id.dsnloc2_id
            record.dsnloc3_id = record.location_id.dsnloc3_id
            record.dsnloc4_id = record.location_id.dsnloc4_id
            record.dsnloc5_id = record.location_id.dsnloc5_id
            record.dsnloc6_id = record.location_id.dsnloc6_id
            record.dsnloc7_id = record.location_id.dsnloc7_id
            record.dsnloc8_id = record.location_id.dsnloc8_id
            
    @api.multi
    @api.depends('product_id')
    def _compute_category_levels(self):
        for record in self:
            record.dsncat1_id = record.product_id.dsncat1_id
            record.dsncat2_id = record.product_id.dsncat2_id
            record.dsncat3_id = record.product_id.dsncat3_id
            record.dsncat4_id = record.product_id.dsncat4_id
            record.dsncat5_id = record.product_id.dsncat5_id

    dsnloc1_id = fields.Many2one('stock.location',
                             string='Loc1',
                             compute='_compute_location_levels',
                             store=True)

    dsnloc2_id = fields.Many2one('stock.location',
                             string='Loc2',
                             compute='_compute_location_levels',
                             store=True)

    dsnloc3_id = fields.Many2one('stock.location',
                             string='Loc3',
                             compute='_compute_location_levels',
                             store=True)

    dsnloc4_id = fields.Many2one('stock.location',
                                 string='Loc4',
                                 compute='_compute_location_levels',
                                 store=True)

    dsnloc5_id = fields.Many2one('stock.location',
                                 string='Loc5',
                                 compute='_compute_location_levels',
                                 store=True)

    dsnloc6_id = fields.Many2one('stock.location',
                                 string='Loc6',
                                 compute='_compute_location_levels',
                                 store=True)

    dsnloc7_id = fields.Many2one('stock.location',
                                 string='Loc7',
                                 compute='_compute_location_levels',
                                 store=True)

    dsnloc8_id = fields.Many2one('stock.location',
                                 string='Loc8',
                                 compute='_compute_location_levels',
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

    dsnlife_date = fields.Datetime(related='lot_id.life_date', readonly=True)
    dsnremoval_date = fields.Datetime(related='lot_id.removal_date', readonly=True)

    qty = fields.Float(string='Quantity',
                   required=True,
                   help="Quantity of products in this quant, in the default unit of measure of the product",
                   readonly=True,
                   select=True,
                   digits=dp.get_precision('Stock Weight'))