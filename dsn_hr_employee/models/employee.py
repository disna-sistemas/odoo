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

class employee(models.Model):
    _inherit = "hr.employee"

    dsn_nif = fields.Char(string="NIF")
    dsn_ssn = fields.Char(string="SS Nr", help="SS Number")
    dsn_street = fields.Char(string="Street")
    dsn_zip = fields.Char(string="Zip")
    dsn_city = fields.Char(string="City")
    dsn_mobile = fields.Char(string="Mobile")
    dsn_ssquotgroup = fields.Integer(string="SS Quotation Group")
    dsn_email = fields.Char(string="e-mail", groups="base.group_hr_user")
    dsn_joiningdate = fields.Date(string="Joining Date")
    dsn_notes = fields.Text(string="Notes")
    dsn_anviz_userid = fields.Text(string="anviz user id")

