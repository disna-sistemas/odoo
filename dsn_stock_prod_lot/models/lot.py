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

from openerp import models, fields, api, _, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

class dsnStockProductionLot(models.Model):
    _inherit = ['stock.production.lot']

    @api.multi
    @api.depends('name')
    def _compute_lot_code(self):
        for record in self:
            _lot = record.name
            _longitud = _lot.length
            if _lot.contains('_'):
                _long =_lot.find('_',0)
                if _long > 0:
                    _longitud = _long -1
            record.dsn_lot_code = _lot[0:_longitud]

    @api.multi
    @api.depends('life_date')
    def _compute_dsn_life_date(self):
        for record in self:
            days_to_add = 0
            if record.life_date:
                hora = datetime.strptime(record.life_date, "%Y-%m-%d %H:%M:%S").hour
                if hora > 21:
                    days_to_add=1

                record.dsn_life_date = datetime.strptime(record.life_date, "%Y-%m-%d %H:%M:%S") + relativedelta(days=days_to_add)

#    @api.multi
#    def _compute_semi_lots(self):
#        for record in self:
#            if record.id:
#                track_obj = self.env['mrp.track.lot']
#                track_lst = track_obj.search([('product_lot', '=', record.id),
#                                              ('component.product_tmpl_id.dsncat2_id.name','=','SEMI')])
#                if track_lst:
#                    record.dsn_semi_comp_unique_lot_ids = track_lst.mapped('component_lot')


    dsn_lot_code = fields.Char(string='Official Lot Name',
                               compute='_compute_lot_code',
                               store=True,
                               help='Lot name for sale purposes:  picking, invoice, certificate, ...')

    dsn_comp_lot_ids = fields.One2many(comodel_name='mrp.track.lot',
                                       inverse_name='product_lot',
                                       string='Lots',
                                       readonly=True)
#semi
#    dsn_semi_comp_unique_lot_ids = fields.One2many(comodel_name='stock.production.lot', compute='_compute_semi_lots',string='semi_lots',store=True)

    @api.multi
    def _get_picking_ids(self):
        for record in self:
            if record.id:
                sale_obj = self.env['sale.order']
    #            op_obj = self.env['stock.pack.operation']
                sale_lst = sale_obj.search([('invoice_ids', '=',
                                             record.id)])
                record.dsn_picking_ids = sale_lst.mapped('picking_ids')
    #            op_lst = op_obj.search([('product_id', '=', self.product_id.id),
    #                                    ('picking_id', 'in',
    #                                     pickings.ids)])





    dsn_life_date = fields.Date(string='Life Date 2', compute='_compute_dsn_life_date', store=True)

    @api.model
    def create(self, values):
        res=super(dsnStockProductionLot, self).create(values)

        return res


    @api.multi
    def write(self, values):
        res = super(dsnStockProductionLot, self).write(values)
        if self.env.user.id!=1:
            if 'country_ids' in values:
                _message = "Lot " + self.name + "- Countries modified: "
                _body = ''
                for country in self.country_ids:
                    _body += ('<b> * %s:</b> %s-%s: <i>%s</i><br>' %
                             (country.country_id.name, country.date_from or '', country.date_to or '', country.notes or ''))

                _body = (_('<b>%s</b><br>%s<br>') % (_message, _body))

                mail_mail = self.env['mail.mail']
                mail_id = mail_mail.create({
                    'model': 'stock.production.lot',
                    'res_id': self.id,
                    'record_name': 'Lot control',
                    'email_from': self.env['mail.message']._get_default_from(),
    #                'email_to': 'vmartinper@gmail.com',
    #                'email_cc': 'vicktormartin@gmail.com',
                    'reply_to': self.env['mail.message']._get_default_from(),
                    'subject': _('Countries modified on Lot: % s') % (self.name),
                    'body_html': '%s' % _body,
                    'auto_delete': True,
                    'message_id': self.env['mail.message']._get_message_id({'no_auto_thread': True}),
                    'partner_ids': [(4, id.id) for id in self.message_follower_ids],
                })
                mail_mail.send([mail_id])

        return res

    @api.multi
    @api.onchange('product_id','removal_date')
    def dsn_check_fields(self):
        self.ensure_one()
        res = {}
        if self.product_id:
            _removal_date_warning = False
            _other_lots = ''
            if self.removal_date:
                lot_obj = self.env['stock.production.lot']
                lots = lot_obj.search([('product_id','=',self.product_id.id),
                                       ('quant_ids.qty','>',0),
                                       ('quant_ids.location_id.usage','=','internal'),
                                       ('removal_date','>',self.removal_date)])
                for lot in lots:
                    _other_lots = _other_lots + "," + lot.name
            else:
                # Mostrar warning si no es p.a.
                if self.product_id.product_tmpl_id.dsncat2_id[0][0] != 7:
                    _removal_date_warning = True

            if _removal_date_warning:
                res = {'warning': {'title': _('Missing removal date'), 'message': _(
                    'Lot should have a removal date.')}}

            else:
                if len(_other_lots) > 0:
                    res = {'warning': {'title': _('There are some lots expiring later'), 'message': _(
                        _other_lots)}}

        return res


    @api.multi
    def button_unlock(self):
        res = super(dsnStockProductionLot, self).button_unlock()

        if self.locked == False:
            if self.product_id.product_tmpl_id.product_brand_id.name == 'CS':
                _subject = "Lot " + self.name + " unblocked by " + self.write_uid.name
                _body = '<div><p>who: ' + self.write_uid.name + '<br>when: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '</p></div>'

#                res_partner_obj = self.env['res.partner']
#                partner_cc_id = res_partner_obj.search([('email','=','sistemas@disna.com')], limit=1)
#                for id in partner_cc_id:
#                    self.message_follower_ids.append(id)

#                partner_obj = self.env['res.partner']
#                partner_ids = partner_obj.search([('email', '=', 'sistemas@disna.com')])
#                new_follower_ids = [p.id for p in partner_ids if p not in self.message_follower_ids]
#                self.message_subscribe([self.id], partner_ids)

                mail_mail = self.env['mail.mail']
                mail_id = mail_mail.create({
                    'model': 'stock.production.lot',
                    'res_id': self.id,
                    'record_name': _('Unblocking'),
                    'email_from': self.env['mail.message']._get_default_from(),
                    'email_to': 'ventas@disna.com',
#                    'email_cc': 'sistemas@disna.com',
                    'reply_to': self.env['mail.message']._get_default_from(),
                    'subject': _(_subject),
                    'body_html': '%s' % _body,
                    'auto_delete': True,
                    'message_id': self.env['mail.message']._get_message_id({'no_auto_thread': True}),
                    'partner_ids': [(4, id.id) for id in self.message_follower_ids],
                })
                mail_mail.send([mail_id])

        return res

    _sql_constraints = [
        ('name_product_uniq', 'unique(name, product_id)', 'Lot Name must be unique per product !!!'),
]