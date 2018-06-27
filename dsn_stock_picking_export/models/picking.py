# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP SA (<http://openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _, exceptions
from datetime import datetime
import sys
import xml.etree.ElementTree as etree

import ftplib





class dsnStockPickingExport(models.Model):
    _inherit = "stock.picking"

    def replace_bars(self, cadena):
        while cadena.find(chr(92)) != -1:
            cadena = cadena.replace(chr(92),"_")

        while cadena.find(chr(47)) != -1:
            cadena = cadena.replace(chr(47), "_")

        return cadena

    @api.multi
    def dsn_button_stock_picking_export_file(self):

        param_obj = self.env['ir.config_parameter']
        local_folder_ids = param_obj.search([('key', '=', 'disna.local.folder')])

        if local_folder_ids:
            local_folder_id = local_folder_ids[0]
            local_folder = local_folder_id['value']
        else:
            raise exceptions.Warning(_('Local folder not defined'))

        for record in self:

            _name = self.replace_bars(record.name)

            xsi = "http://www.w3.org/2001/XMLSchema-instance"
            xsd = "http://www.w3.org/2001/XMLSchema"
            ns = {"xmlns:xsi": xsi, "xmlns:xsd": xsd}
            for attr, uri in ns.items():
                etree.register_namespace(attr.split(":")[1], uri)

            sale_order_model = self.env['sale.order']
            cond = [('name', '=', record.origin)]
            sale_orders = sale_order_model.search(cond)
            sale_order_ref = record.origin
            if sale_orders:
                for sale_order in sale_orders:
                    if sale_order.client_order_ref:
                        sale_order_ref = sale_order.client_order_ref

            alb = etree.Element("alb",
                                dict(user=record.write_uid.name,
                                     file_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  # put `**ns))` if xsi, xsd are unused

            _dsnidcli = ""
            if record.partner_id.dsnidcli:
                _dsnidcli = self.replace_bars(str(record.partner_id.dsnidcli))
            docdata = etree.SubElement(alb, "doc",
                {
                    "name": _name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "disna_order": record.origin, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "date": record.date, etree.QName(xsi, "type"): etree.QName(xsd, "dateTime"),
                    "partner_id": str(record.partner_id.id), etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_dsnidcli": _dsnidcli, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_name": record.partner_id.name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_street": record.partner_id.street, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_zip": record.partner_id.zip, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_city": record.partner_id.city, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_country": record.partner_id.country_id.name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "sale_comment": record.sale_comment, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "client_order_ref": str(sale_order_ref), etree.QName(xsi, "type"): etree.QName(xsd, "string")
                })

            for prod in record.move_lines.mapped('product_id'):
                _dsnidart = ""
                if prod.dsnidart:
                    _dsnidart = self.replace_bars(str(prod.dsnidart))

#                for line in record.move_lines.filtered(lambda x: x.product_id == prod):

    #                for quant in line.reserved_quant_ids.mapped('lot_id'):
                for lot in record.move_lines.reserved_quant_ids.mapped('lot_id'):
                    lotdata = etree.SubElement(docdata, "lot",
                           {
                               "product_id": str(lot.product_id.id), etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "product_code": lot.product_id.default_code, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "product_dsnidart": _dsnidart, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "product_name": lot.product_id.product_tmpl_id.dsn_name_es, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "lot_name": lot.name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
#                               "lot_qty": str(sum(quant.qty)), etree.QName(xsi, "type"): etree.QName(xsd, "string")
                               "lot_qty": str(sum(record.move_lines.reserved_quant_ids.filtered(lambda x: x.lot_id == lot).mapped('qty')))
                           })

            etree.ElementTree(alb).write(local_folder + _name + '.xml', xml_declaration=True)

        self.dsn_export_file = True

        return True

#   Esta función agrupa por producto y excluye campos de Marino
    @api.multi
    def dsn_button_stock_picking_export2_file(self):

        param_obj = self.env['ir.config_parameter']
        local_folder_ids = param_obj.search([('key', '=', 'disna.local.folder')])

        if local_folder_ids:
            local_folder_id = local_folder_ids[0]
            local_folder = local_folder_id['value']
        else:
            raise exceptions.Warning(_('Local folder not defined'))

        for record in self:

            _name = self.replace_bars(record.name)

            xsi = "http://www.w3.org/2001/XMLSchema-instance"
            xsd = "http://www.w3.org/2001/XMLSchema"
            ns = {"xmlns:xsi": xsi, "xmlns:xsd": xsd}
            for attr, uri in ns.items():
                etree.register_namespace(attr.split(":")[1], uri)

            sale_order_model = self.env['sale.order']
            cond = [('name', '=', record.origin)]
            sale_orders = sale_order_model.search(cond)
            sale_order_ref = record.origin
            if sale_orders:
                for sale_order in sale_orders:
                    if sale_order.client_order_ref:
                        sale_order_ref = sale_order.client_order_ref

            alb = etree.Element("alb",
                                dict(user=record.write_uid.name,
                                     file_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  # put `**ns))` if xsi, xsd are unused
            docdata = etree.SubElement(alb, "doc",
                {
                    "name": _name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "disna_order": record.origin, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "date": record.date, etree.QName(xsi, "type"): etree.QName(xsd, "dateTime"),
                    "partner_name": record.partner_id.name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_street": record.partner_id.street, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_zip": record.partner_id.zip, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_city": record.partner_id.city, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "partner_country": record.partner_id.country_id.name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "sale_comment": record.sale_comment, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                    "client_order_ref": str(sale_order_ref), etree.QName(xsi, "type"): etree.QName(xsd, "string")
                })

            quant_ids = self.env['stock.quant'].search([('reservation_id.picking_id.id','=',record.id)]).sorted(key=lambda x: (x.product_id.default_code, x.lot_id.name))

            prod_code = ""
            prod_name = ""
            lot_name = ""
            qty = 0
            for quant in quant_ids:
                if quant.lot_id.name==lot_name and quant.product_id.default_code==prod_code:
                    qty += quant.qty
                else:
                    if prod_code != "":
                        lot = etree.SubElement(docdata, "lot",
                           {
                               "product_code": prod_code, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "product_name": prod_name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "lot_name": lot_name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                               "lot_qty": str(qty), etree.QName(xsi, "type"): etree.QName(xsd, "string")
                           })

                    qty = quant.qty
                    prod_code = quant.product_id.default_code
                    prod_name = quant.product_id.product_tmpl_id.dsn_name_es
                    lot_name = quant.lot_id.name

            if prod_code != "":
                lot = etree.SubElement(docdata, "lot",
                   {
                       "product_code": prod_code, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                       "product_name": prod_name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                       "lot_name": lot_name, etree.QName(xsi, "type"): etree.QName(xsd, "string"),
                       "lot_qty": str(qty), etree.QName(xsi, "type"): etree.QName(xsd, "string")
                   })

            etree.ElementTree(alb).write(local_folder + _name + '.xml', xml_declaration=True)

        self.dsn_export_file = True

        return True

    @api.multi
    def dsn_button_export_to_ftp(self):

        param_obj = self.env['ir.config_parameter']
        ftp_server_ids = param_obj.search([('key', '=', 'disna.ftp.server')])
        ftp_user_ids = param_obj.search([('key', '=', 'disna.ftp.user')])
        ftp_pwd_ids = param_obj.search([('key', '=', 'disna.ftp.pwd')])
        local_folder_ids = param_obj.search([('key', '=', 'disna.local.folder')])

        if ftp_server_ids:
            ftp_server_id = ftp_server_ids[0]
            ftp_server = ftp_server_id['value']
        else:
            raise exceptions.Warning(_('No ftp server defined'))

        if ftp_user_ids:
            ftp_user_id = ftp_user_ids[0]
            ftp_user = ftp_user_id['value']
        else:
            raise exceptions.Warning(_('Ftp user not defined'))

        if ftp_pwd_ids:
            ftp_pwd_id = ftp_pwd_ids[0]
            ftp_pwd = ftp_pwd_id['value']
        else:
            raise exceptions.Warning(_('Ftp password not defined'))

        if local_folder_ids:
            local_folder_id = local_folder_ids[0]
            local_folder = local_folder_id['value']
        else:
            raise exceptions.Warning(_('Local folder not defined'))

        self.dsn_button_stock_picking_export_file()

        for record in self:
            _name = self.replace_bars(record.name)
            ftp = ftplib.FTP(ftp_server, ftp_user, ftp_pwd)
            file = open(local_folder + _name + ".xml", "r")
            ftp.storbinary("STOR " + _name + ".xml", file)
            file.close()
            ftp.quit()

        return True

    dsn_export_file = fields.Boolean(string="Exportado",
                                     default=False)





