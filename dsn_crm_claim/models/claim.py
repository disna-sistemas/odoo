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

from openerp import models, fields

class partner(models.Model):
    _inherit = "crm.claim"

    time=fields.Integer(string="Time", help="Tiempo imputable (hh:mm)")
    cost=fields.Float(string="Cost", help="Coste en euros asociado")

    dsn_partner_ids = fields.Many2many(comodel_name="res.partner",
                                       relation="dsn_claim_partner_rel",
                                       column1="claim_id",
                                       columns2="partner_id",
                                       string="Partners")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    dsn_claims = fields.One2many('crm.claim', 'partner_id', string='Claims')
