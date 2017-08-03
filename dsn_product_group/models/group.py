# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Group(models.Model):
    _name='dsngroup'

    code=fields.Char(string='Code',
                     size=5,
                     required=True,
                     company_dependent=False
                     )

    name=fields.Char(string='Name',
                     size=50,
                     required=True,
                     company_dependent=False
                     )