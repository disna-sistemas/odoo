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

from openerp import models, fields, api, exceptions
from datetime import datetime
import logging

class ProductTemplateSpecs(models.Model):
    _name="dsn.product.template.specifications"

    product_tmpl_id = fields.Many2one(comodel_name="product.template", string="Product Template")
    country_id = fields.Many2one(comodel_name="res.country", string="Country")

    prod_specs = fields.Char(string="Product Specifications")
    label_specs = fields.Char(string="Label Specifications")
    name = fields.Char(string="Register Name")

    title1 = fields.Char(string="Reg1")
    from1 = fields.Date(string="From1")
    until1 = fields.Date(string="Until1")

    title2 = fields.Char(string="Reg2")
    from2 = fields.Date(string="From2")
    until2 = fields.Date(string="Until2")

    notes = fields.Char(string="Notes")


class ProductTemplate(models.Model):
    _inherit = "product.template"

#    @api.multi
#    def dsn_user_allowed_to_edit(self):
#        self.ensure_one()
#        ret = False
#        if self.product_manager and self.product_manager.id == self.uid:
#            ret = True
#        return ret


#    @api.multi
#    @api.depends('seller_ids.product_code')
#    def _compute_dsn_codes(self):
#        _logger = logging.getLogger(__name__)
#        for record in self.seller_ids.filtered(lambda x: x.name == 151 or x.name == 499):
#            for prodselinfo in record.seller_ids:
#                if prodselinfo.name == 151:
#                    record.dsn_code_difusion = prodselinfo.product_code
#                if prodselinfo.name == 499:
#                    _logger.info('CODE ' + prodselinfo.product_code)
#                    record.dsn_code_vileda = prodselinfo.product_code

    @api.multi
    def write(self, values):

        allow_update = True
        _updated_fields = ""
        _usr_mgr_comparison = ""

        _uid = self.env.uid

        for record in self:
            if allow_update and _uid != 1:

                if record.product_manager:

                    if record.product_manager.id != _uid:

                        _forbidden_fields = ['active', 'alert_time', 'categ_id', 'color', 'description', 'description_purchase', 'description_sale',
                            'dsn_name_es', 'dsn_name_en', 'dsn_pnt_esp', 'dsn_pnt_nf', 'dsn_standard', 'dsn_weight_type', 'dsn_weight_type_margin',
                            'hr_expense_ok', 'intrastat_id', 'is_label', 'loc_case', 'life_time', 'list_price',
                            'loc_rack', 'loc_row', 'machine_ok', 'manufacturer', 'manufacturer_purl', 'manufacturer_pname',
                            'manufacturer_pref', 'mes_type', 'name', 'no_create_variants', 'product_brand_id', 'product_manager', 'product_type',
                            'purchase_line_warn_msg', 'produce_delay', 'purchase_ok', 'purchase_requisition', 'raw_material', 'reference_mask',
                            'removal_time', 'rental', 'sale_delay', 'sale_ok', 'sale_line_warn_msg', 'state', 'uom_id', 'uom_po_id', 'uop_id',
                            'uos_coeff', 'uos_id', 'use_time', 'track_all', 'track_incoming', 'track_outgoing', 'track_production', 'type',
                            'volume', 'warranty', 'weight', 'weight_net', 'dsn_length', 'dsn_width', 'dsn_height', 'dsn_net_volume',
                            'dsn_box_prefer_desc1', 'dsn_box_prefer_desc_en','dsn_box_weight', 'dsn_box_length', 'dsn_box_width', 'dsn_box_height',
                            'dsn_box_volume', 'dsn_box_barcode', 'dsn_box_units', 'dsn_box_config', 'dsn_super_box_barcode', 'dsn_super_box_units',
                            'dsn_super_box_config']


                        for _field in _forbidden_fields:
                            if _field in values:

                                _updated_fields = _updated_fields + _field + ","
                                _usr_mgr_comparison = 'usr ' + str(_uid) + ', mngr ' + str(record.product_manager.id)

                                allow_update = False

                                break

                else: #Force to define a product manager
                    if 'product_manager' not in values:
                        raise exceptions.Warning('You must specify the product manager')


        if allow_update:
            return super(ProductTemplate, self).write(values)
        else:
           raise exceptions.Warning('You are not allowed to modify this product template!!! (' + _updated_fields + ') ' + _usr_mgr_comparison)


    dsn_pnt_nf = fields.Char(string='PNT NF')
    dsn_pnt_esp = fields.Char(string='PNT ESP')

    dsn_rinsing = fields.Boolean(string='Rinsing', default=True)

    dsn_spec_ids = fields.One2many(comodel_name="dsn.product.template.specifications", inverse_name="product_tmpl_id", string="Template Specs")

    dsn_hs_code = fields.Char(string='H.S. Code')

#    dsn_pictogram1 = fields.Binary(string='Pictogram 1')
#    dsn_pictogram2 = fields.Binary(string='Pictogram 2')
#    dsn_pictogram3 = fields.Binary(string='Pictogram 3')


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    @api.depends('default_code')
    def _compute_default_code(self):
        for record in self:
            record.default_code=record.default_code.upper()

    @api.multi
    @api.depends('dsnidart')
    def _compute_dsnidart(self):
        for record in self:
            record.dsnidart=record.dsnidart.upper()

    @api.multi
    def write(self, values):

        allow_update = True
        _updated_fields = ""

        _uid = self.env.uid


        for record in self:
            if allow_update and _uid != 1 and record.product_tmpl_id.product_manager:

                if record.product_tmpl_id.product_manager.id != _uid:

                    _forbidden_fields = ['active', 'adr_class_id','default_code','description','dsnidart','dsn_box_barcode',
                    'dsn_box_config','dsn_box_units','dsn_brand_id','dsn_calc_cost','ean13','manual_code',
                    'name','name_template','product_id','weight','weight_net','volume']

                    for _field in _forbidden_fields:
                        if _field in values:
                            _updated_fields = _updated_fields + _field + ","
                            allow_update = False

        #                    a = datetime.strptime(self.create_date, "%Y-%m-%d %H:%M:%S")
        #                    b = datetime.now()
        #                    diff = (b-a).total_seconds()
        #                    if diff>3600:
        #                        if self.product_tmpl_id.product_manager == self.env.user:
        #                            _allow_update = True
                            break

        if allow_update:
            return super(ProductProduct, self).write(values)
        else:
            raise exceptions.Warning('You are not allowed to modify this product!!! (' + _updated_fields + ')')


    dsn_code_difusion = fields.Char(string='Difusion Code', store=True)

    dsn_code_vileda = fields.Char(string='Vileda Code', store=True)

    # dsn_lots = fields.One2many(comodel_name='stock.production.lot', inverse_name='product_id',
    #                            string='Lots', help='Lots related to this product')

    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', 'Product Code must be unique!!!'),
        ('dsnidart_uniq', 'unique(dsnidart)', 'Marino Id must be unique!!!'),
    ]


class dsnProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.onchange('product_code')
    def onchange_lang_es_ES(self):
        self.ensure_one()
#        result={}
        if self.name.id == 151:
            self.product_id.write({'dsn_code_difusion': self.product_code})
        if self.name.id == 499:
#            result.update({'product_tmpl_id.dsn_code_vileda': self.product_code})
            self.product_id.write({'dsn_code_vileda': self.product_code})

#        return result
