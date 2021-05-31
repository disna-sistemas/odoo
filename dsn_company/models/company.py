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
import logging

class dsnCompany(models.Model):
    _inherit = "res.company"

    _logger = logging.getLogger(__name__)

    @api.multi
    def dsn_button_do_work(self):
        lista = ['4749S','4750S','4747S','4748S']

        prodobj = self.env['product.product']
        for cod in lista:
            prods = prodobj.search([('default_code','=',cod)])
            if prods:
                prod = prods[0]
                prodvs = prodobj.search([('default_code', '=', cod + 'V')])
                if prodvs:
                    prodv = prodvs[0]
                    ctrylist = []
                    for pavc in prod.country_list:
                        ident = prodv.country_list.create({'product_id': prodv.product_id, 'country_id': pavc.country_id,
                                                           'cc': pavc.cc, 'date_to': pavc.date_to, 'date_from': pavc.date_from}).id
                        ctrylist.append(ident)
#                    print lista
                    prodv.country_list = [6, 0, ctrylist]

                    _logger.info('ASIGNADOs países de ' + prodv)

        return True

    dsn_logo2 = fields.Binary('Logo Instituto Naturvita', help='Logo for certificates')
    dsn_logo_export = fields.Binary('Export Logo for documents', help='Logo for export docs')
    dsn_logo_docs = fields.Binary('Logo for documents', help='Logo for documents')
 