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

from openerp import models, fields, api, _

class dsnCompany(models.Model):
    _inherit = "res.company"

    dsn_logo2 = fields.Binary('Logo Instituto Naturvita', help='Logo for certificates')
    dsn_logo_export = fields.Binary('Export Logo for documents', help='Logo for export docs')
    dsn_logo_docs = fields.Binary('Logo for documents', help='Logo for documents')
 