from odoo import api, fields, models

class EncryptedPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    encrypted_data = fields.Text('Encrypted Data', readonly=True)
    access_key = fields.Char('Access Key', readonly=True)



