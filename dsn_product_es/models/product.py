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
import logging

#class ProductTemplateTranslation(models.Model):
#    _inherit = "ir.translation"
#
#     @api.multi
#     @api.onchange('src','value')
#     def onchange_lang_es_ES(self):
#         _logger=logging.getLogger(__name__)
#         prod_obj = self.env['product.template']
#
#         for record in self.filtered(lambda x: x.type=='model' and x.name=='product.template,name' and x.lang=='es_ES'):
#             _logger.info('IR TRANSLATION ' + record.name + ' ' + str(record.res_id))
#             prod_ids = prod_obj.search([('id','=',str(record.res_id))])
#             if prod_ids:
#                 prod = prod[0]
#                 _logger.info('PRODUCT' + prod.default_code)
#                 prod.write({'dsn_name_es': record.value,
#                             'dsn_name_en': record.src})
# #                prod.dsn_name_es = record.value
# #                prod.dsn_name_en = record.src

class product(models.Model):

    _inherit = "product.template"

    def _default_translation(self):
        return self.name


    # @api.multi
    # @api.depends('write_date')
    # def dsn_update_es_en_names(self):
    #     translation_obj = self.env['ir.translation']
    #     _logger = logging.getLogger(__name__)
    #     for record in self:
    #         translation_ids = translation_obj.search([('src','=',record.name),
    #                                                   ('name','=','product.template,name'),
    #                                                   ('type','=','model'),
    #                                                   ('lang','=','es_ES')])
    #         if translation_ids:
    #             _logger.info('ENTRANDO')
    #             translation_id=translation_ids=[0]
    #             record.dsn_name_en = record.name
    #             record.dsn_name_es = translation_id.value
    #             _logger.info('updating PRODUCT ' + str(record.id) + ' ' + translation_id.value)

    @api.model
    def dsn_update_es_en_description(self):
        product_obj = self.env['product.template']
        translation_obj = self.env['ir.translation']
        product_ids = product_obj.search(['|',('dsn_name_es','=',False),('dsn_name_en','=',False)])

        _logger = logging.getLogger(__name__)

        if product_ids:
            for product_id in product_ids:

                translat_ids = translation_obj.search([('name','=','product.name,template'),
                                                        ('type','=','model'),
                                                        ('lang','=','es_ES'),
                                                        ('src','=',product_id.name)])
                if translat_ids:
                    translat_es = translat_ids[0].value

                    if translat_es:

                        product_id.write({"dsn_name_es": translat_es,
                                       "dsn_name_en": product_id.name})

                        _logger.info('updting PRODUCT ' + str(product_id.id) + ' ' + translat_es)


    dsn_name_es = fields.Char(string='Traducción ES')

    dsn_name_en = fields.Char(string='English Traduction')


# class IrTranslation(models.model):
#     _inherit = "ir.translation"
#
#     @api.multi
#     def write(self, values):
#         product_obj = self.env['product.template']
#         for record in self:
#             if record.name == "product.template,name" and record.type == 'model' and record.lang == 'es_ES':
#                 _logger = logging.getLogger(__name__)
#                 product_name = record.src
#                 product_ids = product_obj.search([('name','=',product_name)])
#
#                 for product_id in product_ids:
#                     product_id.write({'dsn_name_en': record.src,
#                                       'dsn_name_es': record.value})
#                     _logger.info('updating PRODUCT ' + str(product_id.id) + ' ' + record.value)
#
#                     break
#
#         return super(IrTranslation, self).write(values)