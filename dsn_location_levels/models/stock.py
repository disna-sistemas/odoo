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

class dsnStockLocationLevels(models.Model):
    _inherit = "stock.location"

    @api.multi
    @api.depends('location_id','name')
    def _compute_levels(self):
        for record in self:

            if record:
                testigo = record

                while testigo:
                    record.dsnloc1_id = testigo
                    testigo = testigo.location_id

                # Compute Location 2
                testigo = record
                while testigo.location_id:
                    record.dsnloc2_id = testigo
                    testigo = testigo.location_id

                # Compute Location 3
                testigo = record
                while testigo.location_id.location_id:
                    record.dsnloc3_id = testigo
                    testigo = testigo.location_id

                # Compute Location 4
                testigo = record
                while testigo.location_id.location_id.location_id:
                    record.dsnloc4_id = testigo
                    testigo = testigo.location_id

                # Compute Location 5
                testigo = record
                while testigo.location_id.location_id.location_id.location_id:
                    record.dsnloc5_id = testigo
                    testigo = testigo.location_id

                # Compute Location 6
                testigo = record
                while testigo.location_id.location_id.location_id.location_id.location_id:
                    record.dsnloc6_id = testigo
                    testigo = testigo.location_id

                # Compute Location 7
                testigo = record
                while testigo.location_id.location_id.location_id.location_id.location_id.location_id:
                    record.dsnloc7_id = testigo
                    testigo = testigo.location_id

                # Compute Location 8
                testigo = record
                while testigo.location_id.location_id.location_id.location_id.location_id.location_id.location_id:
                    record.dsnloc8_id = testigo
                    testigo = testigo.location_id

    dsnloc1_id = fields.Many2one('stock.location',
                                string='Loc1',
                                compute='_compute_levels',
                                store=True)

    dsnloc2_id = fields.Many2one('stock.location',
                                 string='Loc2',
                                 compute='_compute_levels',
                                 store=True)

    dsnloc3_id = fields.Many2one('stock.location',
                                 string='Loc3',
                                 compute='_compute_levels',
                                 store=True)

    dsnloc4_id = fields.Many2one('stock.location',
                             string='Loc4',
                             compute='_compute_levels',
                             store=True)

    dsnloc5_id = fields.Many2one('stock.location',
                             string='Loc5',
                             compute='_compute_levels',
                             store=True)

    dsnloc6_id = fields.Many2one('stock.location',
                             string='Loc6',
                             compute='_compute_levels',
                             store=True)

    dsnloc7_id = fields.Many2one('stock.location',
                             string='Loc7',
                             compute='_compute_levels',
                             store=True)

    dsnloc8_id = fields.Many2one('stock.location',
                             string='Loc8',
                             compute='_compute_levels',
                             store=True)