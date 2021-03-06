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
    "name": "Disna - CRM Claim",
    "version": "0.3",
    "author": "Disna, S.A.",
    "contributors": [],
    "website": "",
    "category": "",
    "depends": ['crm_claim','crm_claim_links','product'],
    "description": """
- New relation with partners
- Product link
- Component Link
- Form, Tree and Calendar view customized
    """,
    "data": [
        'views/crm_claim.xml'
    ],
    "installable": True,
    "auto_install": False,
}
