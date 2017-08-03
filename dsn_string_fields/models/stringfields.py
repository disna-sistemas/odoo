# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class dsnStringFields(models.Model):

    _name = 'dsn.string.fields'

    str_invoice = fields.Char(string='Invoice',
                              size=20,
                              default='Invoice')

    str_payment_mode = fields.Char(string='Payment Mode',
                                   size=20,
                                   default='Payment Mode')

    str_payment_term = fields.Char(string='Payment Term',
                                   size=20,
                                   default='Payment Term')

    str_date_due = fields.Char(string='Date Due',
                               size=20,
                               default='Date Due')