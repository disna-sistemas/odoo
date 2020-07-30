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

# Computes the number of the planned_date

from openerp import models, fields, api, exceptions
from datetime import datetime

class dsnMrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def action_assign(self):

        cancel_operation = False

        for record in self:
            if record.project_id is None:
                cancel_operation = True

        if cancel_operation:
            raise exceptions.Warning('Project must be specified')
        else:
            res = super(dsnMrpProduction, self).action_assign()
            self.recalc_production_notes()
            return res

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        res = super(dsnMrpProduction, self).onchange_product_tmpl_id()
        res['domain'].update({
            'bom_id': [('product_tmpl_id', '=', self.product_tmpl_id.id),('state','!=','draft')]})
        return res

    @api.multi
    @api.onchange('date_planned')
    def onchange_date_planned(self):
        for of in self:
            for wl in of.workcenter_lines:
                wl.write({'date_planned': of.date_planned})

class dsnMrpProductionWorkcenterLine(models.Model):
    _inherit = "mrp.production.workcenter.line"

    @api.multi
    @api.onchange('date_planned')
    def onchange_date_planned(self):
        for ot in self:
            ot.production_id.write({'date_planned': ot.date_planned})



#   Imprimir etiquetas
#    @api.multi
#    def dsn_button_print_label(self):
#        for record in self:
#            lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
#            lpr.stdin.write(record.name)
#
#        return True


#    @api.multi
#    @api.depends('date_planned')
#    def _compute_planned_day(self):
#        for record in self:
#            try:
#                record.dsn_planned_day = 99
#                record.dsn_planned_day = record.date_planned.day
#                _d = datetime.strptime(record.date_planned, "%Y-%m-%d %H:%M:%S.%f")
#                record.dsn_planned_day = _d.day
#                break;
#            except ValueError:
#                record.dsn_planned_day = 99

#   dsn_planned_day = fields.Integer(string='Day', compute='_compute_planned_day', store=True)

#    dsn_nr_labels = fields.Integer(string='Number of Labels', compute='_compute_nr_of_labels', store=True)












