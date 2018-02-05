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

class product(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends('write_date')
    def _compute_translations(self):
        for record in self:
#            record.dsn_name_es = record.name
#            record.dsn_name_en = record.name

            translat = self.env['ir.translation'].search(
                        [
                            ('res_id','=',record.id),
                            ('name','=','product.template,name'),
                            ('lang','=','es_ES')
                         ], limit=1
            )
            if translat:
                record.dsn_name_es = translat.value
                record.dsn_name_en = translat.source

#            translat = self.env['ir.translation'].search(
#                [
#                    ('res_id', '=', record.id),
#                    ('name', '=', 'product.template,name'),
#                    ('lang', '=', 'en_US')
#                ], limit=1
#            )

#            if translat:
#                record.dsn_name_en = translat.value

    dsn_name_es = fields.Char(string='Traducción ES',
                              compute='_compute_translations',
                              store=True)

    dsn_name_en = fields.Char(string='English Traduction',
                              compute='_compute_translations',
                              store=True)

