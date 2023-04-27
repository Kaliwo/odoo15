{
    'name': 'Purchase Order Encryption',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Encrypt purchase orders with NEAR blockchain',
    'description': """
Encrypt purchase orders with NEAR blockchain and require an access key for vendors to view them.
    """,
    'author': 'Alinafe Kaliwo',
    'website': 'https://www.mechromalawi.com',
    'depends': ['purchase', 'sale'],
    'data': [
        'views/purchase_order_views.xml',
        'views/purchase_order_access_views.xml',
        'data/email_template_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
