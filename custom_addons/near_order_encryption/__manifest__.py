{
    "name": "NEAR Order Encryption",
    "version": "1.0.0",
    "category": "Sales",
    "summary": "Encrypt Sales and Purchase Orders using NEAR Blockchain",
    "author": "Alinafe Kaliwo",
    "website": "https://www.mechromalawi.com",
    "license": "AGPL-3",
    "depends": ["base", "sale", "purchase"],
    "data": [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/purchase_order_views.xml',
        #'views/purchase_order_line_views.xml',
        'views/email_template.xml',
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
