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
    "name": "Disna - INE Groups",
    "version": "0.1",
    "author": "Disna",
    "contributors": [],
    "website": "",
    "category": "product",
    "depends": ['product','dsn_menu_disna'],
    "description": """
Creates new entity INE and a link from product template
    """,
    "data": [
            'views/group.xml',
            'views/product.xml',
    ],
    "installable": True,
}
