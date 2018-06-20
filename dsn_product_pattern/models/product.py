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

class dsnProductPattern(models.Model):
    _name = 'dsn.product.pattern'

    name = fields.Char(string='Pattern')

    partner_id = fields.Many2one('res.partner',
                                string = 'Customer',
                                domain = [('customer','=',True)])

    product_tmpl_id = fields.Many2one('product.template',
                                      string='Prod.Template')

    component_ids = fields.One2many('dsn.product.pattern.components',
                                    string = 'Components',
                                    inverse_name = 'product_pattern_id')

class dsnProductPatter_Components(models.Model):
    _name = 'dsn.product.pattern.components'

    product_pattern_id = fields.Many2one('dsn.product.pattern',
                                         string = 'Product Pattern',
                                         required = True,
                                         ondelete = 'restrict')

    product_id = fields.Many2one('product.product',
                                 string = 'Product',
                                 required = True,
                                 ondelete = 'restrict')

    version_id = fields.Many2one('product.label.version',
                                 string = 'Version',
                                 ondelete = 'restrict')



