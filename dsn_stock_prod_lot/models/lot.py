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
import logging

class dsnLotSemiLotPA(models.Model):
    _name = 'dsn.lot.father'

    lot_id = fields.Many2one('stock.production.lot')
    father_id = fields.Many2one('stock.production.lot')

class dsnLotComponents(models.Model):
    _name = 'dsn.lot.components'

    lot_id = fields.Many2one('stock.production.lot')
    product_id = fields.Many2one('product.product')
    version_id = fields.Many2one('product.label.version')


class dsnStockProductionLot(models.Model):
    _inherit = ['stock.production.lot']

    @api.multi
    @api.depends('name')
    def _compute_lot_code(self):
        for record in self:
            _lot = record.name
            _longitud = len(_lot)
            _long =_lot.find('_',0)
            if _long > 0:
                _longitud = _long
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

    dsn_life_date = fields.Date(string='Life Date 2', compute='_compute_dsn_life_date', store=True)

#    dsn_lot_cert = fields.Many2one(comodel_name='stock.production.lot', string='Lot certif.')

    # dsn_lot_cert_ids = fields.Many2many(comodel_name="stock.production.lot",
    #                              relation="dsn_lot_lot_cert_rel",
    #                              column1="lot_id",
    #                              column2="lot_cert_id",
    #                              string="Certif. Lots")

    dsn_lot_certif_ids = fields.Many2many(comodel_name='dsn.lot.father',
                                          string='Certif. Lots')

    dsn_component_ids = fields.One2many(comodel_name='dsn.lot.components',
                                        inverse_name='lot_id',
                                         string='Lot Components')

    dsn_production_id = fields.Many2one(comodel_name='mrp.production', string='Producción')

    @api.model
    def create(self, values):

        res = super(dsnStockProductionLot, self).create(values)

        return res


    @api.multi
    def write(self, values):

        res = True

        move_obj = self.env['stock.move']
        production_obj = self.env['mrp.production']

        _logger = logging.getLogger(__name__)

        for record in self:

#Save production_id
            productions = production_obj.search([('move_created_ids2.restrict_lot_id','=',record.id)])
            if productions:
                values['dsn_production_id'] = productions[0].id

#Traceability

            d1 = datetime.strptime(record.create_date, '%Y-%m-%d %H:%M:%S')
            d2 = datetime.strptime(record.write_date,'%Y-%m-%d %H:%M:%S')
            days = (d2-d1).days
            if days < 1200:
                cert_lots=[]
                certif_lots = []
                comps=[]
                compdic={}
                witness_lot = record
                witness_father = record
                lot_and_father = False
                move_obj = self.env['stock.move']
                rl_obj = self.env['mrp.relabel.log']
                production_obj = self.env['mrp.production']
                lotfather_obj = self.env['dsn.lot.father']
                lotcomp_obj = self.env['dsn.lot.components']

                seguir = True
                while seguir:
                    moves = move_obj.search([('restrict_lot_id','=',witness_lot.id),('relabel_dest_id','!=',False)])
                    if moves: #El lote proviene de un relabel
                        move = moves[0]
                        rlogs = rl_obj.search([('relabel_id','=',move.relabel_dest_id.id),('destination_lot_id','=',witness_lot.id)])
                        if rlogs:
                            rlog = rlogs[0]
                            #********************************
                            for c in rlog.component_ids:
                                if c not in comps:
                                    comps.append(c)
                                    compdic[c] = None
                            # ********************************
                            witness_lot = rlog.origin_lot_id
                            witness_father = rlog.origin_lot_id
#                            witness_lot.dsn_father_lot_id = witness_father
                        else: #No debería entrar nunca aquí
                            _logger.info('NO DEBERIA ')
                            pass
                    else:
                        #Añadimos el propio witness y seguimos buscando
                        lot_and_father = lotfather_obj.create({'lot_id': witness_lot.id,
                                                               'father_id': witness_lot.id})
                        certif_lots.append(lot_and_father)
                        #Comprobar si existe una producción que crea el lote
                        moves = move_obj.search([('restrict_lot_id', '=', witness_lot.id), ('production_id', '!=', False)])
                        if moves: # pueden haber más de un stock.move, porque se haya imputado en 2 o 3 quants.  Coger sólo el PRIMERO
                            #**********************************
                            for move in moves:
                                productions = production_obj.search([('id', '=', move.production_id.id)])
                                production = productions[0]
                                for m in productions.move_lines2:
                                    if m.product_id not in comps:
                                        comps.append(m.product_id)
                                        version_id = None
                                        if m.lot_ids:
                                            if m.lot_ids[0].version_id:
                                                version_id = m.lot_ids[0].version_id
                                        compdic[m.product_id] = version_id
                            # **********************************

                            productions = production_obj.search([('id','=',move.production_id.id)])
                            #Siempre debe encontrar una única producción
                            production = productions[0]
                            # Si la producción contiene lotes de SEMI, asignamos el primer lote tiene alguna producción de semi asignar LA PRIMERA.  Si no, continuar búsqueda descendiente
                            semi_moves = production.move_lines2.filtered(lambda x: x.state=='done' and x.product_id.product_tmpl_id.dsncat2_id.name == 'SEMI')
                            if semi_moves:

                                for semi_move in semi_moves:
                                    if semi_move.restrict_lot_id!=witness_lot:
                                        witness_lot = semi_move.restrict_lot_id
#                                        witness_lot.write({'dsn_father_lot_id': witness_father.id })
                                        lot_and_father = lotfather_obj.create({'lot_id': witness_lot.id,
                                                                              'father_id': witness_father.id})
#                                        witness_lot.dsn_father_lot_id = witness_father
#                                        cert_lots.append(witness_lot)
                                        certif_lots.append(lot_and_father)
                                seguir = False

                            else:
                                pa_moves = production.move_lines2.filtered(lambda x: x.state=='done' and x.product_id.product_tmpl_id.dsncat2_id.name in ('PA','SE'))
                                if pa_moves: #PA or SE found
                                    pa_move = pa_moves[0]

                                    witness_lot = pa_move.restrict_lot_id
                                    witness_father = pa_move.restrict_lot_id
#                                    witness_lot.write({'dsn_father_lot_id': witness_father.id})
                                    lot_and_father = lotfather_obj.create({'lot_id': witness_lot.id,
                                                                           'father_id': witness_father.id})

                                    certif_lots.append(lot_and_father)
                                else: #No seguimos buscando, puede ser que la propia OF madre tenga el certificado (tintes, etc...)
                                    seguir = False

                        else: #Nada que hacer, se deja witness_lot tal como está
                            seguir = False

                if len(certif_lots) == 0:
                    lot_and_father = lotfather_obj.create({'lot_id': witness_lot.id,
                                                           'father_id': witness_lot.id})
                    certif_lots.append(lot_and_father)

                values['dsn_lot_certif_ids'] = [(6, 0, [x.id for x in certif_lots])]

                if compdic.items:
                    lot_comps = []
                    for prod,ver in compdic.items():
                        _logger.info(prod.default_code)
                        lot_comp = lotcomp_obj.create({'lot_id': record.id,
                                                        'product_id': prod.id,
                                                        'version_id': None if ver is None else ver.id})
                        lot_comps.append(lot_comp)

                    values['dsn_component_ids'] = [(2, c.id) for c in values['dsn_component_ids'],
                                                                       (6,0, [x.id for x in lot_comps])]

                # if comps:
                #     lot_comps=[]
                #     for x in comps:
                #          if x.default_code is None:
                #              _logger.info(x.name)
                #          else:
                #              _logger.info(x.default_code)
                #
                #          lot_comp = lotcomp_obj.create({'lot_id': record.id,
                #                                        'product_id': x.id})
                #          lot_comps.append(lot_comp)
                #
                #     values['dsn_component_ids'] = [(6, 0, [x.id for x in lot_comps])]

            if res:
                res = super(dsnStockProductionLot, record).write(values)

        if self.env.user.id!=1:
            if 'country_ids' in values:
                _message = "Lot " + self.name + "- Countries modified: "
                _body = ''
                for country in self.country_ids:
                    _body += ('<b> * %s:</b> %s-%s: <i>%s</i><br>' %
                             (country.country_id.name, country.date_from or '', country.date_to or '', country.notes or ''))

                _body = (_('<b>%s</b><br>%s<br>') % (_message, _body))

                mail_mail = self.env['mail.mail']

                for partner in self.message_follower_ids:
                    if partner.email:

                        mail_id = mail_mail.create({
                            'model': 'stock.production.lot',
                            'res_id': self.id,
                            'record_name': 'Lot control',
                            'email_from': self.env['mail.message']._get_default_from(),
                            'email_to': partner.email,
#                            'email_cc': 'vicktormartin@gmail.com',
                            'reply_to': self.env['mail.message']._get_default_from(),
                            'subject': _('Countries modified on Lot: % s') % (self.name),
                            'body_html': '%s' % _body,
                            'auto_delete': True,
                            'message_id': self.env['mail.message']._get_message_id({'no_auto_thread': True}),
#                            'partner_ids': [(4, id.id) for id in self.message_follower_ids],
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