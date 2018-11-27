##########################################################################
#  Copyright (C) 2014  Victor Martin                                     #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
##########################################################################

{
    "name": "Disna - QC Extension",
    "version": "0.1",
    "author": "Disna, S.A.",
    "contributors": [],
    "website": "",
    "category": "",
    "depends": ['quality_control_stock', 'quality_control_mrp',
                'quality_control_mrp_operations','quality_control_claim','quality_control_force_valid',
                'dsn_menu_disna','dsn_security','dsn_product_category_levels'],
    "description": """
QC customization:
- Add internal notes in tree view
- Add button to return to ready state from waiting state in form view
- Analysis Methods
- Etc menu item for test questions
    """,
    "data": [
        'views/qc.xml',
    ],
    "installable": True,
    "auto_install": False,
}
