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
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

class dsnQcTest(models.Model):
    _inherit = "qc.test"

    @api.multi
    @api.depends('object_id')
    def _compute_product(self):
        for record in self:
            if record.object_id and record.object_id.type=='product':
                record.product_id = record.object_id

    product_id = fields.Many2one(string="Product",
                                 comodel_name="product.product",
                                 compute='_compute_product',
                                 store=True)

class dsnQcAnalysisMethod(models.Model):
    _name="dsnqc.analysis.method"

    name = fields.Char(string="Method")
    notes = fields.Text(string="Notes")


class dsnQcTestQuestion(models.Model):
    _inherit = "qc.test.question"

    def get_default_method(self):
        if self.test.category.name == "Certificate":
            return None
        else:
            method_obj=self.env['dsnqc.analysis.method']
            method_lst = method_obj.search([('name','=','Visual Control')])
            if method_lst:
                return method_lst[0]
            else:

                return None



    method_id = fields.Many2one(comodel_name="dsnqc.analysis.method",
                                string="Analysis Method",
                                required=True,
                                default=get_default_method)

    dsn_auto_success = fields.Boolean(string="Auto Success")



class dsnQcInspection(models.Model):
    _inherit = "qc.inspection"

    def _get_language(self):
        lang_obj=self.env['res.lang']
        lang_ids = lang_obj.search([('active','=',True)])
        return [(lang.code, lang.name ) for lang in lang_ids]

    @api.multi
    @api.depends('product')
    def _compute_category_levels(self):
        for record in self:
            record.dsncat2_id = record.product.product_tmpl_id.dsncat2_id

    dsn_date_analysis = fields.Date('Date of Analysis', readonly=True)

    dsn_lang = fields.Selection(_get_language, string='Language')

    dsn_company = fields.Selection([('disna','Disna'),('naturvita','Instituto Naturvita')], default='disna')

    dsncat2_id = fields.Many2one('product.category',
                                 string='Cat2',
                                 compute='_compute_category_levels',
                                 store=True
                                 )

    @api.multi
    def dsn_action_back_to_ready(self):
        self.write({'state': 'ready'})

    @api.multi
    @api.depends('production')
    def _get_production_qty(self):
        for record in self:
            _n = 0
            if record.production:
                _n = record.production.product_qty

            record.dsn_production_qty = _n

    @api.multi
    @api.depends('inspection_lines')
    def _compute_samples(self):
        for record in self:
            _samples = False
            for line in record.inspection_lines.filtered(lambda x: x.name.upper() == "MUESTRAS DE MUESTROTECA"):
                _samples = line.success
            record.dsn_samples = _samples

            _sent = False
            for line in record.inspection_lines.filtered(lambda x: x.name.upper() == "MUESTRAS ENVIADAS"):
                _sent = line.success
            record.dsn_sent_to_micro = _sent

            _micro = False
            for line in record.inspection_lines.filtered(lambda x: x.name.upper() == "MUESTRAS OK MICROBIOLOGIA"):
                _micro = line.success
            record.dsn_micro_ok = _micro

    @api.multi
    def action_confirm(self):
        for inspection in self:

            inspection.dsn_date_analysis = datetime.now()

            notes =""
            for l in inspection.inspection_lines.filtered(lambda x: x.success==False):
                notes = notes + l.name + "\r\n"
            if notes:
                notes = "Acciones Correctivas\r\n\n" + notes + "\r\n"
                inspection.lot.write({'notes': notes})

        result = super(dsnQcInspection, self).action_confirm()
        return result

    dsn_samples = fields.Boolean(string='Samples', default=False, compute='_compute_samples', store=True)
    dsn_sent_to_micro = fields.Boolean(string='Sent to micro', default=False, compute='_compute_samples', store=True)
    dsn_micro_ok = fields.Boolean(string='Micro OK', default=False, compute='_compute_samples', store=True)

    dsn_production_qty = fields.Float(string="Production Qty", compute='_get_production_qty', store=False)


class dsnQcInspectionLine(models.Model):
    _inherit = "qc.inspection.line"

    @api.multi
    @api.depends('test_line')
    def compute_auto_success(self):
        for record in self:
            record.dsn_auto_success = record.test_line.dsn_auto_success
            if record.dsn_auto_success:
                record.success = True

    dsn_auto_success = fields.Boolean(string="Auto Success",
                                      compute='compute_auto_success',
                                      readonly=True)