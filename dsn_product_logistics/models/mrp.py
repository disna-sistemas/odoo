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

class MrpProduction(models.Model):
    _inherit = "mrp.production"

#    @api.multi
#    @api.depends('product_tmpl_id')
#    def _compute_default_packaging(self):

#        for record in self:
#            packaging_ids = record.product_tmpl_id.packagings.filtered(lambda x: x.dsn_default == True).sorted(key=lambda x: x.id, reverse=False)
#            if packaging_ids:
#                record.dsn_packaging_id = packaging_ids[0]

    dsn_packaging_id = fields.Many2one(comodel_name='product.packaging',
                                    string='Packaging',
                                    domain="[('id','in', product_tmpl_id.packagings)]",
#                                    default='_compute_default_packaging',
                                    store=True)

#    @api.multi0
#    @api.depends('product_id')
#    def _compute_possible_packagings(self):
#        for production in self:
#            production.possible_packagings = production.mapped('product_id.product_tmpl_id.packagings')
#
#    possible_packagings = fields.Many2many(comodel_name='product.packaging',
#                                           string='packagingss',
#                                           compute='_compute_possible_packagings')

#    dsn_packaging_id = fields.Many2one(comodel_name='product.packaging',
#                                       domain="[('id', 'in', possible_packagings[0][2])]",
#                                       string='Packaging')

#    @api.multi
#    @api.depends('product_id')
#    def _get_possible_packagings(self):
#        self.ensure_one()
#        for self in self:
#            self.possible_packagings = self.mapped('product_id.product_tmpl_id.packaging_ids')

#    possible_packagings = fields.Many2many(comodel_name='product.packaging',
#                                           compute='_get_possible_packagings')

#    @api.multi
#    @api.depends('routing_wc_line')
#    def _compute_possible_workcenters(self):
#        for line in self:
#            line.possible_workcenters = line.mapped(
#                'routing_wc_line.op_wc_lines.workcenter')

#    possible_workcenters = fields.Many2many(
#        comodel_name="mrp.workcenter", compute="_compute_possible_workcenters")
#    workcenter_id = fields.Many2one(
#        domain="[('id', 'in', possible_workcenters[0][2])]")
