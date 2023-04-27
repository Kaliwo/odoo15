from odoo import models, fields, api

class PurchaseOrderAccess(models.TransientModel):
    _name = 'purchase.order.access'
    _description = 'Purchase Order Access'

    access_key = fields.Char(string='Access Key', required=True)

    def action_access_purchase_order(self):
        # Decrypt the purchase order using the entered access key
        # You'll need to implement this method in the PurchaseOrderEncryption class
        purchase_order = self.env['purchase.order.encryption'].decrypt_purchase_order(self.access_key)

        # Redirect to the decrypted purchase order
        action = self.env.ref('purchase.purchase_order_action_generic').read()[0]
        action['res_id'] = purchase_order.id
        return action
