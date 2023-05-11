# -*- coding: utf-8 -*-

from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    fp700_printer_configuration_id = fields.Many2one(
        'fp700.printer.configuration',
        string='FP700 Printer Configuration',
        help='FP700 fiscal printer configuration for this POS',
    )
