# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    dsn_dateok = fields.Date(string='Date OK', required=False)

    @api.multi
    def write(self, values):
        for record in self:
            if record.move_id:
                record.move_id.write({'dsn_dateok': values['dsn_dateok']})

        return super(AccountInvoice, self).write(values)

    # @api.multi
    # @api.depends('move_id')
    # def _compute_move_dateok(self):
    #     for record in self:
    #         if record.move_id:
    #             record.move_id.write({'dateok': record.dsn_dateok})


class AccountMove(models.Model):
    _inherit = "account.move"

    dsn_dateok = fields.Date(string='Date OK', required=False)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    dsn_dateok = fields.Date(string='Date OK', related="move_id.dsn_dateok", readonly=True)
