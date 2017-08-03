from openerp import models, fields, api
import datetime

class dsnProductAttributeValueCountry(models.Model):

    _inherit = "product.attribute.value.country"

    def get_now(self):
        return datetime.datetime.now()

    @api.multi
    def _compute_now(self):
        self.dsn_now = datetime.datetime.now()

    dsn_now = fields.Datetime(compute = '_compute_now',
                              store=False)
