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

    @api.multi
    def dsn_button_do_work(self):
#        lista = ['4749S','4750S','4747S','4748S','4743S','4744S','4745S','4746S','4677S','4678S','4757S','4758S','4755S','4756S','4751S','4752S','4753S','4754S','4749EP','4750EP','4747EP','4748EP','4743EP','4744EP','4745EP','4746EP','4677EP','4678EP','4757EP','4758EP','4755EP','4756EP','4751EP','4752EP','4753EP','4754EP']
        lista = ['5033S','5034S','5035S','5036S','5045S','5046S','5037S','5038S','2945S','2946S','2951S','2952S','2949S','2950S','2947S','2948S','4180S','4181S']
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
                        ident = prodv.country_list.create({'product_id': prodv.product_id, 'country_id': pavc.country_id.id, 'cc': pavc.cc,
                                                           'date_to': pavc.date_to, 'date_from': pavc.date_from, 'notes': pavc.notes }).id
                        ctrylist.append(ident)
                    prodv.country_list = [(6, 0, ctrylist)]

        return True

    @api.multi
    def dsn_button_mp_assign_coste1(self):

        prodobj = self.env['product.product']

        prods = prodobj.search([('product_tmpl_id.dsncat2_id', '=', 4)])

        for prod in prods:
            if not prod.default_code.upper().startswith('Z'):
                trobat = False
                for catextra in prod.categ_ids:
                    if catextra == 697:
                        trobat = True
                if not trobat:
                    prod.categ_ids = [(4, 697)]

        return True


    dsn_logo2 = fields.Binary('Logo Instituto Naturvita', help='Logo for certificates')
    dsn_logo_export = fields.Binary('Export Logo for documents', help='Logo for export docs')
    dsn_logo_docs = fields.Binary('Logo for documents', help='Logo for documents')
 