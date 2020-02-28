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

    name = fields.Char(string="Operation", required=True)


class dsnMrpBomOperation(models.Model):
    _name = "dsn.mrp.bom.operation"
    _order = "sequence, id"

    bom_id = fields.Many2one(comodel_name='mrp.bom', string='BoM')
    dsnoperation_id = fields.Many2one(comodel_name='dsnoperation', string='Operation')
    sequence = fields.Integer(string='Sequence', required=True)
    description = fields.Text(string='Description')
#    done = fields.Boolean(string='Done')


class dsnMrpBom(models.Model):
    _inherit = "mrp.bom"

    dsn_operation_ids = fields.One2many(comodel_name="dsn.mrp.bom.operation",
                                    inverse_name="dsnoperation_id",
                                    string="Operations")

class dsnMrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    dsnoperation_id = fields.Many2one(comodel_name='dsn.mrp.bom.operation', string='Operation')



class dsnMrpProductionOperation(models.Model):
    _name = "dsn.mrp.production.operation"
    _order = "sequence, id"

    production_id = fields.Many2one(comodel_name='mrp.production', string='OF')
    dsnoperation_id = fields.Many2one(comodel_name='dsnoperation', string='Operation')
    sequence = fields.Integer(string='Sequence', required=True)
    description = fields.Text(string='Description')
    done = fields.Boolean(string='Done')


class dsnMrpProduction(models.Model):
    _inherit = "mrp.production"

    dsn_operation_ids = fields.One2many(comodel_name="dsn.mrp.production.operation",
                                        inverse_name="dsnoperation_id",
                                        string="Operations")


class dsnMrpProductionProductLine(models.Model):
    _inherit = "mrp.production.product.line"

    dsnoperation_id = fields.Many2one(comodel_name='dsn.mrp.production.operation', string='Operation')










