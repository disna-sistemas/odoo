
from openerp import models, fields, api


class dsnOrderPoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"


    _sql_constraints = [
        ('dsn_orderpoint_uniq', 'unique(location_id, company_id, product_id)', 'Order point must be unique per location and product!!!')
    ]