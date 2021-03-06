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

class dsnAccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    @api.one
    @api.depends('parent_id')
    def _compute_level1(self):
        testigo = self

        while testigo:
            self.dsncta1_id = testigo
            testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level2(self):
        levels = 1
        testigo = self

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=2:
            testigo = self
            while testigo.parent_id:
                self.dsncta2_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level3(self):
        levels = 1
        testigo = self

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=3:
            testigo = self
            while testigo.parent_id.parent_id:
                self.dsncta3_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level4(self):
        levels = 1
        testigo = self

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 4:
            testigo = self
            while testigo.parent_id.parent_id.parent_id:
                self.dsncta4_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level5(self):
        levels = 1
        testigo = self

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 5:
            testigo = self
            while testigo.parent_id.parent_id.parent_id.parent_id:
                self.dsncta5_id = testigo
                testigo = testigo.parent_id


    dsncta1_id = fields.Many2one('account.analytic.account',
                                    string='Cta1',
                                    compute='_compute_level1',
                                    store=True)

    dsncta2_id = fields.Many2one('account.analytic.account',
                                    string='Cta2',
                                    compute='_compute_level2',
                                    store=True)

    dsncta3_id = fields.Many2one('account.analytic.account',
                                    string='Cta3',
                                    compute='_compute_level3',
                                    store=True)

    dsncta4_id = fields.Many2one('account.analytic.account',
                                    string='Cta4',
                                    compute='_compute_level4',
                                    store=True)

    dsncta5_id = fields.Many2one('account.analytic.account',
                                    string='Cta5',
                                    compute='_compute_level5',
                                    store=True)