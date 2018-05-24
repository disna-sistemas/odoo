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

class ProductTemplate(models.Model):
    _inherit = "product.template"

    dsn_length = fields.Float("Length", digits=dp.get_precision('cm'), help="Length in cm")
    dsn_width = fields.Float("Width", digits=dp.get_precision('cm'), help="Width in cm")
    dsn_height = fields.Float("Height", digits=dp.get_precision('cm'), help="Height in cm")

class ProductVariant(models.Model):
    _inherit = "product.product"

    @api.multi
    @api.depends('dsn_box_length','dsn_box_width','dsn_box_height')
    def _compute_box_volume(self):
        for record in self:
            record.dsn_box_volume = record.dsn_box_length * record.dsn_box_width * record.dsn_box_height

    dsn_net_volume = fields.Float(string='Net Volume', help='Product volume excluding any packaging')

    dsn_box_barcode = fields.Char(string='Box Barcode',
                                  help='GTIN 14')

    dsn_box_config = fields.Char(string='Box Config',
                                help='Ex: 12 x 300 ml')

    dsn_box_units = fields.Integer(string='Box Units',
                                       help='Number of units per box')

    dsn_box_weight = fields.Float(string="Weight", help="Box total weight in kg")
    dsn_box_length = fields.Float("Length", digits=dp.get_precision('cm'), help="Length in cm")
    dsn_box_width = fields.Float("Width", digits=dp.get_precision('cm'), help="Width in cm")

    dsn_box_volume = fields.Float("Volume",
                                  compute='_compute_box_volume',
                                  digits=dp.get_precision('cm3'),
                                  store=True, help="Volume in cm3")

    dsn_box_height = fields.Float("Height", digits=dp.get_precision('cm'), help="Height in cm")

    dsn_box_prefer_desc1 = fields.Char(string='Preferential description 1 for boxes',
                                         help='Preferential 1st description to be shown in the box label')

    dsn_box_prefer_desc_en = fields.Char(string='Preferential description 2 for boxes',
                                         help='Preferential 2nd description to be shown in the box label')

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    dsn_height = fields.Float('Total Package Height', digits=dp.get_precision('cm'),
                           help='Height of the whole package, pallet or box.')

    dsn_default = fields.Boolean('Default', help='Paletización por defecto')

