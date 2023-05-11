import requests
from odoo import api, fields, models

def encrypt_data(public_key_pem, data):
    response = requests.post('http://localhost:3000/encrypt', json={
        'publicKey': public_key_pem,
        'data': data
    })

    if response.status_code == 200:
        return response.json()['encryptedData']
    else:
        raise ValueError("Encryption failed")

def decrypt_data(private_key_pem, encrypted_data, nonce):
    response = requests.post('http://localhost:3000/decrypt', json={
        'privateKey': private_key_pem,
        'encryptedData': encrypted_data,
        'nonce': nonce
    })

    if response.status_code == 200:
        return response.json()['decryptedData']
    else:
        raise ValueError("Decryption failed")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    public_key = fields.Text(string="Public Key")
    encrypted_private_key = fields.Text(string="Encrypted Private Key")
    passphrase = fields.Char(string="Passphrase")

    def get_customer_private_key(self):
        response = requests.get(f'http://localhost:3000/keys/{self.id}')

        if response.status_code == 200:
            data = response.json()
            return decrypt_data(self.passphrase, data['encryptedPrivateKey'], data['nonce'])
        else:
            raise ValueError("Failed to get private key")

    def set_customer_private_key(self, private_key_pem, passphrase):
        encrypted_private_key = encrypt_data(passphrase, private_key_pem)
        response = requests.post('http://localhost:3000/store-keys', json={
            'accountId': self.id,
            'publicKey': self.public_key,
            'encryptedPrivateKey': encrypted_private_key
        })

        if response.status_code != 200:
            raise ValueError("Failed to store private key")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    encrypted_note = fields.Text(string="Encrypted Note")
    nonce = fields.Char(string="Nonce")

    @api.model
    def create(self, vals):
        customer = self.env['res.partner'].browse(vals['partner_id'])
        print(f"Public Key: {customer.public_key}")  # Add this print statement
        encrypted_data = encrypt_data(customer.public_key, vals.get('note', ''))
        vals['encrypted_note'] = encrypted_data['encryptedData']
        vals['nonce'] = encrypted_data['nonce']
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if 'note' in vals:
            customer = self.partner_id
            encrypted_data = encrypt_data(customer.public_key, vals['note'])
            vals['encrypted_note'] = encrypted_data['encryptedData']
            vals['nonce'] = encrypted_data['nonce']
        return super(SaleOrder, self).write(vals)

    def read(self, fields=None, load="_classic_read"):
        records = super(SaleOrder, self).read(fields, load)
        for record in records:
            if 'encrypted_note' in record:
                customer = self.env['res.partner'].browse(record['partner_id'][0])
                private_key_pem = customer.get_customer_private_key()
                record['note'] = decrypt_data(private_key_pem, record['encrypted_note'], record['nonce'])
        return records

    @api.model
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        template_id = self.env.ref('near_order_encryption.email_template_sale_order_encrypted_note')
        for order in self:
            template_id.send_mail(order.id, force_send=True)
        return res
class AccountMove(models.Model):
    _inherit = 'account.move'

    encrypted_note = fields.Text(string="Encrypted Note")
    nonce = fields.Char(string="Nonce")

    @api.model
    def create(self, vals):
        customer = self.env['res.partner'].browse(vals['partner_id'])
        encrypted_data = encrypt_data(customer.public_key, vals.get('invoice_origin', ''))
        vals['encrypted_note'] = encrypted_data['encryptedData']
        vals['nonce'] = encrypted_data['nonce']
        return super(AccountMove, self).create(vals)

    def write(self, vals):
        if 'invoice_origin' in vals:
            customer = self.partner_id
            encrypted_data = encrypt_data(customer.public_key, vals['invoice_origin'])
            vals['encrypted_note'] = encrypted_data['encryptedData']
            vals['nonce'] = encrypted_data['nonce']
        return super(AccountMove, self).write(vals)

    def read(self, fields=None, load="_classic_read"):
        records = super(AccountMove, self).read(fields, load)
        for record in records:
            if 'encrypted_note' in record:
                customer = self.env['res.partner'].browse(record['partner_id'][0])
                private_key_pem = customer.get_customer_private_key()
                record['invoice_origin'] = decrypt_data(private_key_pem, record['encrypted_note'], record['nonce'])
        return records

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    encrypted_note = fields.Text(string="Encrypted Note")
    nonce = fields.Char(string="Nonce")


    @api.model
    def create(self, vals):
        vendor = self.env['res.partner'].browse(vals['partner_id'])
        encrypted_data = encrypt_data(vendor.public_key, vals.get('notes', ''))
        vals['encrypted_note'] = encrypted_data['encryptedData']
        vals['nonce'] = encrypted_data['nonce']
        return super(PurchaseOrder, self).create(vals)

    def write(self, vals):
        if 'notes' in vals:
            vendor = self.partner_id
            encrypted_data = encrypt_data(vendor.public_key, vals['notes'])
            vals['encrypted_note'] = encrypted_data['encryptedData']
            vals['nonce'] = encrypted_data['nonce']
        return super(PurchaseOrder, self).write(vals)

    def read(self, fields=None, load="_classic_read"):
        records = super(PurchaseOrder, self).read(fields, load)
        for record in records:
            if 'encrypted_note' in record:
                vendor = self.env['res.partner'].browse(record['partner_id'][0])
                private_key_pem = vendor.get_customer_private_key()
                record['notes'] = decrypt_data(private_key_pem, record['encrypted_note'], record['nonce'])
        return records

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    encrypted_name = fields.Text(string="Encrypted Name")
    nonce = fields.Char(string="Nonce")

    @api.model
    def create(self, vals):
        vendor = self.env['res.partner'].browse(vals['partner_id'])
        encrypted_data = encrypt_data(vendor.public_key, vals.get('name', ''))
        vals['encrypted_name'] = encrypted_data['encryptedData']
        vals['nonce'] = encrypted_data['nonce']
        return super(PurchaseOrderLine, self).create(vals)

    def write(self, vals):
        if 'name' in vals:
            vendor = self.partner_id
            encrypted_data = encrypt_data(vendor.public_key, vals['name'])
            vals['encrypted_name'] = encrypted_data['encryptedData']
            vals['nonce'] = encrypted_data['nonce']
        return super(PurchaseOrderLine, self).write(vals)

    def read(self, fields=None, load="_classic_read"):
        records = super(PurchaseOrderLine, self).read(fields, load)
        for record in records:
            if 'encrypted_name' in record:
                vendor = self.env['res.partner'].browse(record['partner_id'][0])
                private_key_pem = vendor.get_customer_private_key()
                record['name'] = decrypt_data(private_key_pem, record['encrypted_name'], record['nonce'])
        return records
