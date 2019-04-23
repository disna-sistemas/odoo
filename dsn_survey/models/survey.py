# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api

class dsnSurveyPage(models.Model):
    _inherit = "survey.page"

    @api.multi
    @api.depends('survey_id.user_input_line_ids')
    def compute_aggregate_functions(self):
        for record in self:
            media = 0
            suma = sum(record.survey_id.user_input_line.filtered(lambda x: x.page_id == record.id).mapped('value_suggested'))
            cuenta = sum(record.survey_id.user_input_line.filtered(lambda x: x.page_id == record.id).mapped(1))
            if (cuenta>0):
                media = suma / cuenta

            dsn_avg_suggested_quizz_mark = media


    dsn_avg_suggested_quizz_mark = fields.Float("Avg Value Suggested",
                          compute='compute_aggregate_functions',
                          store=True)
