from odoo import models, fields, api


class SaleOrderEncryption(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        # Call the super method
        result = super(SaleOrderEncryption, self).create(vals)

        # Generate the access key and send it to the customer
        # This is just a sample implementation; you can customize it as needed
        access_key = self.env['purchase.order.encryption'].generate_access_key()
        result.send_access_key_to_customer(access_key)

        return result


