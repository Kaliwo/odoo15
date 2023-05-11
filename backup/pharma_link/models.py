import os

private_key = os.environ.get('FERNET_SECRET_KEY')
if not private_key:
    raise ValueError("FERNET_SECRET_KEY environment variable is not set.")

from odoo import models, fields, api
from . import near_integration
import json
from cryptography.fernet import Fernet
from datetime import datetime


data = {'timestamp': datetime.now()}
# Convert datetime object to string
data['timestamp'] = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
# Serialize the data
json.dumps(data)

# Your encryption and decryption functions
def some_encryption_function(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def some_decryption_function(data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data.encode()).decode()
    return decrypted_data

# Replace 'your-secret-key' with your actual Fernet secret key
SECRET_KEY = 'L6Dqh4M1oFv-K8AyWKicYUepjFqBoGxtUEhucIIjcD8='
class PharmaLinkSalesOrder(models.Model):
    _name = 'pharma_link.sales.order'
    _description = 'Pharma Link Sales Order'

    name = fields.Char(string='Sales Order Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    order_line = fields.One2many('pharma_link.sales.order.line', 'order_id', string='Order Lines')
    purchase_order_ids = fields.One2many('pharma_link.purchase.order', 'sales_order_id', string='Purchase Orders')

    @api.model
    def create(self, vals):
        # Call the original create method
        record = super().create(vals)

        # Encrypt and store the sales order data on the NEAR blockchain
        data = json.dumps(record.read()[0])  # Serialize the record data
        encrypted_data = some_encryption_function(data)  # Encrypt the data
        near_integration.call_near_interaction_script("store", record.id, encrypted_data, private_key)

        return record
class PharmaLinkPurchaseOrder(models.Model):
    _name = 'pharma_link.purchase.order'
    _description = 'Pharma Link Purchase Order'

    name = fields.Char(string='Purchase Order Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    order_line = fields.One2many('pharma_link.purchase.order.line', 'order_id', string='Order Lines')
    sales_order_id = fields.Many2one('pharma_link.sales.order', string='Sales Order')

class PharmaLinkSalesOrderLine(models.Model):
    _name = 'pharma_link.sales.order.line'
    _description = 'Pharma Link Sales Order Line'

    order_id = fields.Many2one('pharma_link.sales.order', string='Sales Order')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)

class PharmaLinkPurchaseOrderLine(models.Model):
    _name = 'pharma_link.purchase.order.line'
    _description = 'Pharma Link Purchase Order Line'

    order_id = fields.Many2one('pharma_link.purchase.order', string='Purchase Order')
    product_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)
