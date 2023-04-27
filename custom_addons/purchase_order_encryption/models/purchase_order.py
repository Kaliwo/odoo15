from odoo import models, fields, api

class PurchaseOrderEncryption(models.Model):
    _inherit = 'purchase.order'

    encrypted_purchase_order = fields.Binary(string='Encrypted Purchase Order')
    access_key = fields.Char(string='Access Key')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Other code ...

    def send_encryption_key(self):
        # Your implementation for sending the encryption key
        pass