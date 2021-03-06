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

class partner(models.Model):
    _inherit = "crm.claim"

    time=fields.Integer(string="Time", help="Tiempo imputable (hh:mm)")
    cost=fields.Float(string="Cost", help="Coste en euros asociado")

    dsn_product_id = fields.Many2one(comodel_name="product.product",
                                     string="Product",
                                     help="Variante de Producto")
    dsn_component_id = fields.Many2one(comodel_name="product.product",
                                     string="Componente",
                                     help="Componente (Variante de Producto)")

    dsn_partner_ids = fields.One2many(comodel_name="dsn.claim.partner",
                                    inverse_name="claim_id",
                                    string="Partners")

    # categ_ids = fields.Many2many(
    #     comodel_name='product.category', relation='product_categ_rel',
    #     column1='product_id', column2='categ_id', string='Product Categories')

class ClaimPartner(models.Model):
    _name = "dsn.claim.partner"

    claim_id = fields.Many2one(comodel_name="crm.claim", string="Claim", required = True, ondelete='restrict')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required = True, ondelete='restrict')

class Partner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def _compute_claims(self):
        clobj = self.env['crm.claim']

        for record in self:
            cllist = clobj.search(['|', ('dsn_partner_ids.partner_id', '=', record.id),
                                   ('partner_id', '=', record.id)])

            record.dsn_claim_ids = [(6, 0, [x.id for x in cllist])]

            # for claim in cllist:
            #     record.dsn_claim_ids.append(claim)



    dsn_claim_ids = fields.One2many(comodel_name="crm.claim",
                                    string="DSN Claims",
                                    compute="_compute_claims")

class Product(models.Model):
    _inherit = "product.product"

    @api.multi
    def _compute_claims(self):
        clobj = self.env['crm.claim']

        for record in self:
            cllist = clobj.search(['|',('dsn_product_id', '=', record.id),
                                   ('dsn_component_id', '=', record.id)])

            record.dsn_claim_ids = [(6, 0, [x.id for x in cllist])]

    dsn_claim_ids = fields.One2many(comodel_name="crm.claim",
                                    string="DSN Claims",
                                    compute="_compute_claims")