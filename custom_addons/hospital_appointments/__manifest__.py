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
    'name': "Patient Appointment Management",
    'summary': """Patient Appointment""",
    'description': """Patient Appointment""",
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    "license": "AGPL-3",
    'category': 'Hospital',
    'version': '15.0.1.0.0',
    'depends': ['website_sale', 'base_hospital_management'],
    'data': ['security/ir.model.access.csv',
             'reports/patient_card.xml',
             'reports/card_template.xml',
             'reports/patient_card_back.xml',
             'data/appointment_seq.xml',
             'data/mail_template.xml',
             'data/appointment_cancel_template.xml',
             'data/doctor_seq.xml',
             'views/hospital_appointments.xml',
             'views/snippets.xml',
             'views/website_menu.xml',
             'views/appointment.xml',
             'views/thanks.xml',
             'views/doctor.xml',
             ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
