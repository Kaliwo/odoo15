# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "Patient Portal",
    'summary': """
     Displays patient information for the patient portal 
        """,
    'description': """
        Displays patient information for the patient portal
    """,
    'author': "Mechro Limited",
    'company': "Mechro Limited",
    'maintainer': 'Mechro Limited',
    'website': "https://www.mechromalawi.com",
    "license": "AGPL-3",
    'category': 'Portal',
    'version': '15.0.1.0.0',
    'depends': ['base_hospital_management', 'hospital_lab_tests', 'portal'],
    'data': [
        'views/patient_portal_template.xml'
    ]
}
