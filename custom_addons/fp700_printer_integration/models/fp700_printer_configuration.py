from odoo import models, fields

class FP700PrinterConfiguration(models.Model):
    _name = 'fp700.printer.configuration'
    _description = 'FP700 Printer Configuration'

    name = fields.Char(string='Name', required=True)
    serial_port = fields.Char(string='Serial Port', required=True)
    baud_rate = fields.Integer(string='Baud Rate', required=True, default=115200)
    # Add other configuration fields if necessary
