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

from openerp import models, fields, api
import exceptions
import openerp.addons.decimal_precision as dp
from datetime import datetime
#from dateutil.relativedelta import relativedelta


class dsnMp(models.Model):
    _inherit = ['mail.thread']
    _name = 'dsnmp'


    product_id = fields.Many2one(string="Product", comodel_name="product.template", required=True)
    name = fields.Char(string="INCI", required=True)
    anexos = fields.Char(string="Anexos")

    ld50 =fields.Integer(string="LD50")
    noael = fields.Float(string="NOAEL")
    natural =fields.Float(string="% Natural")

    show_on_label = fields.Boolean(string="Show on label")
    extract = fields.Boolean(string="Extract")
    bio = fields.Boolean(string="BIO")
    tested_on_animals = fields.Boolean(string="Tested on Animals")
    tested_on_animals_text = fields.Text(string="")
    update_date = fields.Date("Update Date")

    supplier_ids = fields.Many2many(comodel_name="res.partner",
                                    relation="dsnmp_supplier_rel",
                                    column1="dsmp_id",
                                    column2="partner_id",
                                    string="Suppliers")

    ingredient_ids = fields.One2many(comodel_name="dsnmp.ingredient", inverse_name="mp_id", string="Ingredients")
    cas_ids = fields.One2many(comodel_name="dsnmp.cas", inverse_name="mp_id", string="CAS")
    einec_ids = fields.One2many(comodel_name="dsnmp.einec", inverse_name="mp_id", string="EINECS/ELINCS")

    absouv = fields.Boolean("Absorción UV")
    accabe = fields.Boolean("Acond. Cabello")
    acpiel = fields.Boolean("Acond. Piel")
    alisan = fields.Boolean("Alisante")
    anaglu= fields.Boolean("Antiaglutinante")
    ancasp= fields.Boolean("Anticaspa")
    ancorr= fields.Boolean("Anticorrosivo")
    anespu= fields.Boolean("Antiespumante")
    anesta= fields.Boolean("Antiestatico")
    anmicr= fields.Boolean("Antimicrobiano")
    anoxid= fields.Boolean("Antioxidante")
    anplac= fields.Boolean("Antiplaca")
    astrin= fields.Boolean("Astringente")
    blanqu= fields.Boolean("Blanqueante")
    calman= fields.Boolean("Calmante")
    colora= fields.Boolean("Colorante")
    conser= fields.Boolean("Conservante")
    ctvisc= fields.Boolean("Control Viscosidad")
    cuoral= fields.Boolean("Cuidado Oral")
    desnat = fields.Boolean("Desnaturalizante")
    desodo = fields.Boolean("Desodorante")
    disolv = fields.Boolean("Disolvente")
    edulco = fields.Boolean("Edulcorante")
    emolie = fields.Boolean("Emoliente")
    emulsi = fields.Boolean("Emulsionante")
    enmasc = fields.Boolean("Enmascarante")
    espuma = fields.Boolean("Espumante")
    estemu = fields.Boolean("Estabilizador Emulsión")
    fiform = fields.Boolean("Film Forming")
    fijcab = fields.Boolean("Fijador Cabello")
    filtuv= fields.Boolean("Filtro UV")
    hidrat = fields.Boolean("Hidratante")
    humect = fields.Boolean("Humectante")
    imespu= fields.Boolean("Impulsor Espuma")
    limpia= fields.Boolean("Limpiador")
    opacif= fields.Boolean("Opacificante")
    perfum= fields.Boolean("Perfume")
    plasti= fields.Boolean("Plastificante")
    prpiel= fields.Boolean("Protector Piel")
    quelan= fields.Boolean("Quelante")
    querat= fields.Boolean("Queratolítico")
    reduct = fields.Boolean("Reductor")
    refres= fields.Boolean("Refrescante")
    solubi= fields.Boolean("Solubilizante")
    tampon= fields.Boolean("Tampón")
    tensoa= fields.Boolean("Tensoactivo")
    tonico= fields.Boolean("Tónico")

    toxicity = fields.Text(string="Toxicity Data")
    usage_warning = fields.Text(string="Warning")
    cir = fields.Text(string="CIR")
    other = fields.Text(string="Other")
    security = fields.Text(string="security")

    @api.multi
    @api.constrains('natural')
    def _check_percent(self):
        for record in self:
            if record.natural<0 or record.natural>100:
                raise exceptions.Warning("% Natural is a percentage")

    @api.multi
    @api.depends('product_id')
    def _compute_code(self):
        for record in self:
            record.code=record.product_id.default_code


    code = fields.Char(string='Code',
                                  compute='_compute_code',
                                  store=True)

    @api.multi
    @api.depends('absouv','accabe','acpiel','alisan','anaglu','ancasp','ancorr','anespu','anesta','anmicr','anoxid','anplac','astrin','blanqu',
    'calman','colora','conser','ctvisc','cuoral','desnat','desodo','disolv','edulco','emolie','emulsi','enmasc','espuma','estemu',
    'fiform','fijcab','filtuv','hidrat','humect','imespu','limpia','opacif','perfum','plasti','prpiel','quelan','querat','reduct',
    'refres','solubi','tampon','tensoa','tonico')
    def _compute_functions(self):
        for record in self:
            _fun = ""

            if record.absouv:
                _fun = _fun + "Absorción UV, "
            if record.accabe:
                _fun = _fun + "Acond.Cabello, "
            if record.acpiel:
                _fun = _fun + "Acond.Piel, "
            if record.alisan:
                _fun = _fun + "Alisante, "
            if record.anaglu:
                _fun = _fun + "Antiaglutinante, "
            if record.ancasp:
                _fun = _fun + "Anticaspa, "
            if record.ancorr:
                _fun = _fun + "Anticorrosivo, "
            if record.anespu:
                _fun = _fun + "Antiespumante, "
            if record.anesta:
                _fun = _fun + "Antiestático, "
            if record.anmicr:
                _fun = _fun + "Antimicrobiano, "
            if record.anoxid:
                _fun = _fun + "Antioxidante, "
            if record.anplac:
                _fun = _fun + "Antiplaca, "
            if record.astrin:
                _fun = _fun + "Astringente, "
            if record.blanqu:
                _fun = _fun + "Blanqueante, "
            if record.calman:
                _fun = _fun + "Calmante, "
            if record.colora:
                _fun = _fun + "Colorante, "
            if record.conser:
                _fun = _fun + "Conservante, "
            if record.ctvisc:
                _fun = _fun + "Control Viscosidad, "
            if record.cuoral:
                _fun = _fun + "Cuidado Oral, "
            if record.desnat:
                _fun = _fun + "Desnaturalizante, "
            if record.desodo:
                _fun = _fun + "Desodorante, "
            if record.disolv:
                _fun = _fun + "Disolvente, "
            if record.edulco:
                _fun = _fun + "Edulcorante, "
            if record.emolie:
                _fun = _fun + "Emoliente, "
            if record.emulsi:
                _fun = _fun + "Emulsionante, "
            if record.enmasc:
                _fun = _fun + "Enmascarante, "
            if record.espuma:
                _fun = _fun + "Espumante, "
            if record.estemu:
                _fun = _fun + "Estabilizador Emulsión, "
            if record.fiform:
                _fun = _fun + "Film Forming, "
            if record.fijcab:
                _fun = _fun + "Fijador Cabello, "
            if record.filtuv:
                _fun = _fun + "Filtro UV, "
            if record.hidrat:
                _fun = _fun + "Hidratante, "
            if record.humect:
                _fun = _fun + "Humectante, "
            if record.imespu:
                _fun = _fun + "Impulsor Espuma, "
            if record.limpia:
                _fun = _fun + "Limpiador, "
            if record.opacif:
                _fun = _fun + "Opacificante, "
            if record.perfum:
                _fun = _fun + "Perfume, "
            if record.plasti:
                _fun = _fun + "Plastificante, "
            if record.prpiel:
                _fun = _fun + "Protector Piel, "
            if record.quelan:
                _fun = _fun + "Quelante, "
            if record.querat:
                _fun = _fun + "Queratolítico, "
            if record.reduct:
                _fun = _fun + "Reductor, "
            if record.refres:
                _fun = _fun + "Refrescante, "
            if record.solubi:
                _fun = _fun + "Solubilizante, "
            if record.tampon:
                _fun = _fun + "Tampón, "
            if record.tensoa:
                _fun = _fun + "Tensoactivo, "
            if record.tonico:
                _fun = _fun + "Tónico, "

            record.functions = _fun

    functions = fields.Char(string="Functions", compute='_compute_functions', store=True)


    @api.multi
    def load_ingredients_in_chatter(self, message='Modified Ingredients:'):
        self.ensure_one()
        body = ''

        right_now = datetime.now()

        for ingredient in self.ingredient_ids:

#            diff = ahora - ingredient.write_date

            diff_in_secs = (right_now - datetime.strptime(ingredient.write_date, "%Y-%m-%d %H:%M:%S")).total_seconds()

            if diff_in_secs < 5:

                body += ('<b> * %s:</b> conc.min. %s ; conc.max. %s ; conc.fix. %s <br>' %
                     (ingredient.name.encode('utf-8'), str(round(ingredient.conc_min,4)).encode('utf-8'),
                      str(round(ingredient.conc_max,4)).encode('utf-8'),
                      str(round(ingredient.conc_fixed,4)).encode('utf-8')))

        if len(body)>0:
            m = ('<b>%s</b><br>%s<br>') % (message, body)

            mail_values = {
                'notification': True,
                'model': self._model,
                'res_id': self.id,
            }

            self.message_post(body=m, type='notification', **mail_values)

    @api.multi
    def write(self, values):
        res = super(dsnMp, self).write(values)
        if 'ingredient_ids' in values:
            for record in self:
                record.load_ingredients_in_chatter()
        return res

class dsnMpIngredient(models.Model):
    _name="dsnmp.ingredient"
    _inherit = ['mail.thread']


    @api.multi
    @api.depends('conc_min','conc_max')
    def _compute_conc_avg(self):
        for record in self:
            record.conc_avg=(record.conc_min+record.conc_max)/2

    mp_id = fields.Many2one(string="MP", comodel_name="dsnmp", required=False, ondelete='restrict')

    mp_code = fields.Char(string="MP Code", related="mp_id.product_id.default_code", readonly=True)
    mpingr_id = fields.Many2one(string="Ingredient", comodel_name="dsnmp", required=True, ondelete='restrict')
    name = fields.Char(string="Inci", related="mpingr_id.name", readonly=True)
    mpingr_code = fields.Char(string="Ingr Code", related="mpingr_id.product_id.default_code", readonly=True)
    conc_min = fields.Float(string="Conc.Mín.",digits=dp.get_precision('Product Unit of Measure'))
    conc_max = fields.Float(string="Conc.Máx.",digits=dp.get_precision('Product Unit of Measure'))
    conc_avg = fields.Float(string="Conc.Media",digits=dp.get_precision('Product Unit of Measure'),
                            compute='_compute_conc_avg',readonly=True,store=True)
    conc_fixed = fields.Float(string="Conc.Fija",digits=dp.get_precision('Product Unit of Measure'),
                              readonly=True)

class dsnMpCas(models.Model):
    _name="dsnmp.cas"

    mp_id = fields.Many2one(comodel_name="dsnmp", required=False, ondelete='restrict')

    description = fields.Char(string="CAS")

class dsnMpEinec(models.Model):
    _name = "dsnmp.einec"

    mp_id = fields.Many2one(comodel_name="dsnmp", required=False, ondelete='restrict')
    description = fields.Char(string="EINEC")

class dsnCosmeticSafetyGroup(models.Model):

    _name="dsn.cosmetic.safety.group"

    name=fields.Char(string="Safety Evaluation Group")

    absorption_percen = fields.Integer(string='Absorption %')
    retention_factor = fields.Float(string='Retention Factor', digits=(16, 2))
    daily_exposure = fields.Float(string='Calculated daily exposure (g.day)', digits=(16, 3))
    relative_daily_exposure = fields.Float(string='A (calculated relative daily exposure)', digits=(16, 2))

    surface_area = fields.Float(string='Surface Area', digits=(16,2))
    frequency_application = fields.Float(string='Frequency of Application', digits=(16,2))
    estim_daily_amount_applied = fields.Float(string='Estimated daily amount applied', digits=(16,2))
    relative_amount_applied = fields.Float(string='Relative amount applied', digits=(16, 2))
    notes = fields.Text(string='Notes')

class dsnProductMps(models.Model):
    _inherit = "product.template"

    dsnmp_ids = fields.One2many(comodel_name="dsnmp", inverse_name="product_id", string="mps", ondelete='restrict')

    dsn_cosmetic_safety_group = fields.Many2one(comodel_name="dsn.cosmetic.safety.group",
                                            string="Safety Evaluation Group",
                                            ondelete="restrict",
                                            groups="dsn_security.imasd_manager")
