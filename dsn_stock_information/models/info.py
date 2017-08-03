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

class dsnStockInfo(models.Model):
    _inherit = 'stock.information'

    @api.multi
    @api.depends('location')
    def _compute_locations(self):

        for record in self:

            record.dsnloc1_id = record.location.dsnloc1_id
            record.dsnloc2_id = record.location.dsnloc2_id
            record.dsnloc3_id = record.location.dsnloc3_id
            record.dsnloc4_id = record.location.dsnloc4_id
            record.dsnloc5_id = record.location.dsnloc5_id

    # stock_information
#    qty_available = fields.Float(store=True)
#    minimum_rule = fields.Float(store=True)
    incoming_pending_amount = fields.Float(store=True)
    stock_availability = fields.Float(store=True)
    demand = fields.Float(store=True)
    draft_purchases_amount = fields.Float(store=True)
    draft_sales_amount = fields.Float(store=True)
    outgoing_pending_amount = fields.Float(store=True)
    virtual_stock = fields.Float(store=True)

    # stock_information_mrp
    incoming_pending_amount_moves = fields.Float(store=True)
    incoming_pending_amount_purchases = fields.Float(store=True)
    incoming_pending_amount_productions = fields.Float(store=True)
    draft_productions_amount = fields.Float(store=True)

    #stock_information_mrp_procurement_plan
    incoming_pending_amount_plan = fields.Float(store=True)
    incoming_pending_amount_plan_reservation = fields.Float(store=True)
    outgoing_pending_amount_moves = fields.Float(store=True)
    outgoing_pending_amount_reserv = fields.Float(store=True)

    dsnloc1_id = fields.Many2one(string="Loc1", comodel_name='stock.location', compute='_compute_locations', store=True)
    dsnloc2_id = fields.Many2one(string="Loc2", comodel_name='stock.location', compute='_compute_locations', store=True)
    dsnloc3_id = fields.Many2one(string="Loc3", comodel_name='stock.location', compute='_compute_locations', store=True)
    dsnloc4_id = fields.Many2one(string="Loc4", comodel_name='stock.location', compute='_compute_locations', store=True)
    dsnloc5_id = fields.Many2one(string="Loc5", comodel_name='stock.location', compute='_compute_locations', store=True)




