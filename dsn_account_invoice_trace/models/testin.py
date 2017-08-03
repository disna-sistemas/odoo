#!/usr/bin/env python
from openerp import models, fields, api


class some(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_pickings(self):
        for record in self:
            if record.id:
                sale_obj = self.env['sale.order']
                #            op_obj = self.env['stock.pack.operation']
                sale_lst = sale_obj.search([('invoice_ids', '=',
                                             record.id)])
                print sale_lst
