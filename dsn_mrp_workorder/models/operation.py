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
from datetime import datetime

class OperationTimeLine(models.Model):
    _inherit = 'operation.time.line'


    def _default_time(self):
        return datetime.now().strftime("%Y-%m-%d")
#        return datetime.now()

    @api.multi
    @api.depends('operation_time')
    def _compute_production(self):
        for record in self:
            record.production=record.operation_time.production_id

    start_date = fields.Datetime(string='Start Date', default=_default_time)
    end_date = fields.Datetime(string='End Date', default=_default_time)
    production = fields.Many2one('mrp.production', string='Production', compute='_compute_production', store=True)

