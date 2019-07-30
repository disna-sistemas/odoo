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

class dsnProjectTask(models.Model):
    _inherit = "project.task"

    dsn_product_tmpl_id = fields.Many2one(comodel_name='product.template',
                                          string='Product Template',
                                          required=False)



class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _compute_tasks(self):
        taskobj = self.env['project.task']

        for record in self:
            tasklist = taskobj.search([('dsn_product_tmpl_id', '=', record.id)])

            record.dsn_task_ids = [(6, 0, [x.id for x in tasklist])]

    dsn_task_ids = fields.One2many(comodel_name="project.task",
                                    string="DSN Project Tasks",
                                    compute="_compute_tasks")
