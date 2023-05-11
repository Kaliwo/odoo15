# -*- coding: utf-8 -*-
{
    'name': 'FP700 Printer Integration',
    'version': '1.0.0',
    'category': 'Hardware',
    'summary': 'Integration of Datecs FP700 fiscal printer with Odoo 16',
    'author': 'Alinafe Kaliwo',
    'website': 'https://www.mechromalawi.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'point_of_sale',  # If you're integrating with Odoo's Point of Sale module
        'sale',  # If you're integrating with Mechro AoB's Sales module
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fp700_printer_configuration_views.xml',
        'views/pos_config_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'pyserial',
            'qrcode',
        ],
    },
}
