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


class ProductLabelVersion(models.Model):
    _inherit = 'product.label.version'

    @api.model
    def create(self, values):

        for record in self:

            _subject = "New product version:  " + record.name

            _body = "Product "

            if record.product_id.default_code:
                _subject +=" - Product " + record.product_id.default_code
                _body += "Product code: " + record.product_id.default_code

            _body += "<br>Product ES name: " + record.product_id.product_tmpl_id.dsn_name_es
            _body += "<br>Version: " + record.name

            mail_mail = self.env['mail.mail']

            for partner in self.message_follower_ids:
                if partner.email:
                    mail_id = mail_mail.create({
                        'model': 'stock.production.lot',
                        'res_id': self.id,
                        'record_name': 'Product Version',
                        'email_from': self.env['mail.message']._get_default_from(),
                        'email_to': 'technical@disna.com',
                        'reply_to': self.env['mail.message']._get_default_from(),
                        'subject': _subject,
                        'body_html': '%s' % _body,
                        'auto_delete': True,
                        'message_id': self.env['mail.message']._get_message_id({'no_auto_thread': True}),
                        'partner_ids': [(4, id.id) for id in self.message_follower_ids],
                    })
                    mail_mail.send([mail_id])

        res = super(ProductLabelVersion, self).create(values)

        return res

