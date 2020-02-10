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

class dsnProductTemplateCategoryLevels(models.Model):
    _inherit = "product.template"

    @api.one
    @api.depends('categ_id')
    def _compute_level1(self):
        testigo = self.categ_id

        while testigo:
            self.dsncat1_id = testigo
            testigo = testigo.parent_id

    @api.one
    @api.depends('categ_id')
    def _compute_level2(self):
        levels = 1
        testigo = self.categ_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=2:
            testigo = self.categ_id
            while testigo.parent_id:
                self.dsncat2_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('categ_id')
    def _compute_level3(self):
        levels = 1
        testigo = self.categ_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=3:
            testigo = self.categ_id
            while testigo.parent_id.parent_id:
                self.dsncat3_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('categ_id')
    def _compute_level4(self):
        levels = 1
        testigo = self.categ_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 4:
            testigo = self.categ_id
            while testigo.parent_id.parent_id.parent_id:
                self.dsncat4_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('categ_id')
    def _compute_level5(self):
        levels = 1
        testigo = self.categ_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 5:
            testigo = self.categ_id
            while testigo.parent_id.parent_id.parent_id.parent_id:
                self.dsncat5_id = testigo
                testigo = testigo.parent_id


    dsncat1_id = fields.Many2one('product.category',
                                    string='Cat1',
                                    compute='_compute_level1',
                                    store=True)

    dsncat2_id = fields.Many2one('product.category',
                                    string='Cat2',
                                    compute='_compute_level2',
                                    store=True)

    dsncat3_id = fields.Many2one('product.category',
                                    string='Cat3',
                                    compute='_compute_level3',
                                    store=True)

    dsncat4_id = fields.Many2one('product.category',
                                 string='Cat4',
                                 compute='_compute_level4',
                                 store=True)

    dsncat5_id = fields.Many2one('product.category',
                                 string='Cat5',
                                 compute='_compute_level5',
                                 store=True)




class dsnProductCategoryLevels(models.Model):
    _inherit = "product.category"

    @api.one
    @api.depends('parent_id')
    def _compute_level1(self):
        testigo = self.parent_id

        while testigo:
            self.dsncat1_id = testigo
            testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level2(self):
        levels = 1
        testigo = self.parent_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=2:
            testigo = self.parent_id
            while testigo.parent_id:
                self.dsncat2_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level3(self):
        levels = 1
        testigo = self.parent_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >=3:
            testigo = self.parent_id
            while testigo.parent_id.parent_id:
                self.dsncat3_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level4(self):
        levels = 1
        testigo = self.parent_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 4:
            testigo = self.parent_id
            while testigo.parent_id.parent_id.parent_id:
                self.dsncat4_id = testigo
                testigo = testigo.parent_id

    @api.one
    @api.depends('parent_id')
    def _compute_level5(self):
        levels = 1
        testigo = self.parent_id

        while testigo:
            testigo = testigo.parent_id
            levels += 1

        if levels >= 5:
            testigo = self.parent_id
            while testigo.parent_id.parent_id.parent_id.parent_id:
                self.dsncat5_id = testigo
                testigo = testigo.parent_id


    dsncat1_id = fields.Many2one('product.category',
                                    string='Cat1',
                                    compute='_compute_level1',
                                    store=True)

    dsncat2_id = fields.Many2one('product.category',
                                    string='Cat2',
                                    compute='_compute_level2',
                                    store=True)

    dsncat3_id = fields.Many2one('product.category',
                                    string='Cat3',
                                    compute='_compute_level3',
                                    store=True)

    dsncat4_id = fields.Many2one('product.category',
                                 string='Cat4',
                                 compute='_compute_level4',
                                 store=True)

    dsncat5_id = fields.Many2one('product.category',
                                 string='Cat5',
                                 compute='_compute_level5',
                                 store=True)
