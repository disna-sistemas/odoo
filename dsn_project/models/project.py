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

class dsnProject(models.Model):
    _inherit = "project.project"

    dsn_product_tmpl_id = fields.Many2one(comodel_name='product.template',
                                          string='Product Template',
                                          required=False)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _compute_projects(self):
        projobj = self.env['project.project']

        for record in self:
            projlist = projobj.search([('dsn_product_tmpl_id', '=', record.id)])

            record.dsn_project_ids = [(6, 0, [x.id for x in projlist])]

    dsn_project_ids = fields.One2many(comodel_name="project.project",
                                    string="DSN Projects",
                                    compute="_compute_projects")
