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

# Computes the number of the planned_date

from openerp import models, fields, api, exceptions
from datetime import datetime


class dsnMrpOperations(models.Model):
    _name = "dsnoperation"


class mrpBomDsnOperation(models.Model):
    _name = "mrp.bom.dsnoperation"
    _order = 'sequence, id'

    name = fields.Char(string="Operation", required=True)
    bom_id = fields.Many2one(comodel_name='mrp.bom', string='BoM')
    dsnoperation_id = fields.Many2one(comodel_name='dsnoperation', string='Operation')
    sequence = fields.Integer(string='Sequence', required=True)
    description = fields.Text(string='Description')
    done = fields.Boolean(string='Done')



class dsnMrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        res = super(dsnMrpProduction, self).onchange_product_tmpl_id()
        res['domain'].update({
            'bom_id': [('product_tmpl_id', '=', self.product_tmpl_id.id),('state','!=','draft')]})
        return res





