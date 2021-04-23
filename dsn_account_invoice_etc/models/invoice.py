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


class AccountMove(models.Model):
    _inherit="account.move"

    dsn_dateok = fields.Date(string='Date OK', compute='_compute_invoice', store=True)

    @api.multi
    @api.depends('create_date')
    def _compute_invoice(self):
        invoiceobj = self.env['account.invoice']
        for record in self:
            invoices = invoiceobj.search([('move_id', '=', record.id)])
            if invoices:
                record.dsn_dateok = invoices[0].dsn_dateok


