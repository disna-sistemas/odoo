# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP SA (<http://openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from datetime import datetime


class dsnTrademark(models.Model):
    _name="dsn.trademark"

    name = fields.Char("Trademark")


class dsnTrademarkRegistration(models.Model):
    _name="dsn.trademark.registration"


    trademark_id = fields.Many2one(comodel_name="dsn.trademark",string='Trademark')
    country_id = fields.Many2one(comodel_name="res.country", string='Country')

    name = fields.Char('Registration name')

    num_class= fields.Integer("Num.Class")
    type = fields.Selection(['Denominativa','Frasco','Mixta','Palabra'],required=True)

    logo = fields.Binary('Logo')

    request_date_ = fields.Date('Request Date')
    due_date = fields.Date('Due Date')

    state = fields.Selection(
        [('titulo', 'Título'), ('tramite', 'Trámite'), ('pendiente titulo', 'Pendiente Título'),
         ('solicitada', 'Solicitada'), ('cancel', 'Cancelada')], string='State', default='tramite')



