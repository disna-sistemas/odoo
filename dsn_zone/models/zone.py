# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Zone(models.Model):
    _name='zone'

    name=fields.Char(string='Name',
                     size=20,
                     required=True,
                     company_dependent=False
                     )

    parent=fields.Many2one(string='Parent',
                    comodel_name='zone')


