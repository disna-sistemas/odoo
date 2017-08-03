# -*- encoding: utf-8 -*-

from openerp import models, fields, api
import number_to_letter
import datetime

class PaymentOrder(models.Model):
    _inherit='payment.order'

    @api.one
    @api.depends('total')
    def _amount_to_words(self):
        self.dsn_amount_in_words = number_to_letter.to_word(self.total, 'EUR')


    @api.one
    @api.depends('date_prefered','write_date','date_scheduled')
    def _get_expiration(self):

        d = self.dsn_expiration = datetime.datetime.now()
        self.dsn_expiration = d.replace(year = d.year - 30)

        if self.date_prefered == 'now':
            self.dsn_expiration = self.write_date

        if self.date_prefered == 'fixed':
            self.dsn_expiration = self.date_scheduled

        if self.date_prefered == 'due':
            if self.line_ids:
                for line in self.line_ids:
                    if line.ml_maturity_date > self.dsn_expiration or not self.dsn_expiration:
                        self.dsn_expiration = line.ml_maturity_date

    dsn_amount_in_words = fields.Char(string='Amount in Words',
                                      compute='_amount_to_words',
                                      store=True)

    dsn_expiration = fields.Date(string='Expiration',
                                 compute='_get_expiration',
                                 store=True)


