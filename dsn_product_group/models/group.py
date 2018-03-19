# -*- encoding: utf-8 -*-

from openerp import models, fields

# class Group(models.Model):
#     _name='dsngroup'
#
#     code=fields.Char(string='Code',
#                      size=5,
#                      required=True,
#                      company_dependent=False
#                      )
#
#     name=fields.Char(string='Name',
#                      size=50,
#                      required=True,
#                      company_dependent=False
#                      )

class IneGroup(models.Model):
    _name = "dsninegroup"

    name = fields.Char(string='Name',
                     required=True,
                     company_dependent=False
                     )