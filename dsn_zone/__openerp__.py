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
    "name": "Zone",
    "version": "0.1",
    "author": "Disna",
    "contributors": [],
    "website": "",
    "category": "zone",
    "depends": [],
    "description": """
        Creates new entity zone.  A zone instance can be either a small location,
        a city, a community, a big extension, a continent, ...

        A zone can be defined within another zone.

        Also extends res.partner to make possible to link a partner to a zone.
    """,
    "data": [
            'views/zone.xml',
            'views/partner.xml',
            'security/zone.xml',
    ],
    "installable": True,
}
