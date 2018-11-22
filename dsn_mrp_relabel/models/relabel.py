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

class dsnRelabelLog(models.Model):
    _inherit = 'mrp.relabel.log'

    @api.multi
    @api.depends('product_id', 'relabel_id')
    def _compute_registration(self):

        for record in self:
            _reg = ''
            for spec in record.dsn_spec_ids.filtered(lambda x: x.country_id.id==x.relabel.id_country_id.id):
                _reg = spec.name
            record.dsn_registration = _reg

    dsn_registration = fields.Char(string='Registration', compute='_compute_registration', store=True)

