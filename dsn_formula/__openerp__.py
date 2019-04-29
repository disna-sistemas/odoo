# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Disna Formulas',
    'version': '1.0',
    'category': '',
    'description': """
Creates new entity dsnmp (raw material) and its chemical composition with technical specificacions as
INCI name, NOAEL, LD50, CAS, EINECS, etc...

""",
    'author': 'Disna',
    'website': 'http://www.disna.com',
    'contributors': ["Victor Martin <vicktormartin@gmail.com"],
    'depends': ['mail','product','dsn_product_etc'],
    'data': [
        'views/formula.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
