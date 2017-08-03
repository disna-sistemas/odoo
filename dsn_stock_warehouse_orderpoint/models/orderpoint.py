
from openerp import models, fields, api


class dsnOrderPoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"



    dsn_missing_qty = fields.Float(string='Missing Qty', compute='_compute_missing')
    dsn_missing_virtual_qty = fields.Float(string='Missing Forecast', compute='_compute_missing')

    @api.multi
    @api.depends('product_min_qty','product_location_qty','virtual_location_qty')
    def _compute_missing(self):
        for record in self:
            if record.product_min_qty> record.product_location_qty:
                record.dsn_missing_qty = record.product_min_qty - record.product_location_qty
            else:
                record.dsn_missing_qty = 0

            if record.product_min_qty > record.virtual_location_qty:
                record.dsn_missing_virtual_qty = record.product_min_qty - record.virtual_location_qty
            else:
                record.dsn_missing_virtual_qty = 0
