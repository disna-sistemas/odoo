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

from openerp import models, fields

class dsnReactor(models.Model):
    STATE_SELECTION = [
        ('noOF', 'No OF'),
        ('elaboration', 'In elaboration'),
        ('qc_waiting', 'QC Waiting'),
        ('100', '100%'),
        ('75', '75%'),
        ('50', '50%'),
        ('25', '25%'),
        ('0', '0%'),
    ]

    READONLY_STATES = {
        'elaboration': [('readonly', True)],
        'qc_waiting': [('readonly', True)],
        '100': [('readonly', True)],
        '75': [('readonly', True)],
        '50': [('readonly', True)],
        '25': [('readonly', True)],
        '0': [('readonly', True)],
    }

    _name = "dsn.reactor"

    name = fields.Char(string="Reactor")
    state = fields.Integer(string="Status", readonly=True, default=1)

    order = fields.Many2one(string="OF", comodel_name="mrp.production")

    image1 = fields.Binary(string="No OF")
    image2 = fields.Binary(string="Elaboration")
    image3 = fields.Binary(string="Waiting for QC%")
    image4 = fields.Binary(string="100%")
    image5 = fields.Binary(string="75%")
    image6 = fields.Binary(string="50%")
    image7 = fields.Binary(string="25%")
    image8 = fields.Binary(string="0%")






