# -*- coding: utf-8 -*-

from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders):
        order_ids = super(PosOrder, self).create_from_ui(orders)
        fp700_printer = self.env['fp700.printer']

        for order_id in order_ids:
            order = self.browse(order_id)
            printer_config = order.config_id.fp700_printer_configuration_id
            if printer_config:
                ticket_data = self.prepare_ticket_data(order)
                fp700_printer.print_ticket(printer_config, ticket_data)

        return order_ids

    def prepare_ticket_data(self, order):
        # Company and order information
        company = order.company_id
        company_info = {
            'name': company.name,
            'address': company.street,
            'city': company.city,
            'state': company.state_id.name,
            'zip': company.zip,
            'phone': company.phone,
            'vat': company.vat,
        }

        # Order lines
        order_lines = []
        for line in order.lines:
            order_lines.append({
                'product_name': line.product_id.name,
                'quantity': line.qty,
                'price': line.price_unit,
                'discount': line.discount,
                'tax': line.tax_ids.compute_all(line.price_unit)['total_included'],
                'subtotal': line.price_subtotal_incl,
            })

        # Total and tax amounts
        total_amount = order.amount_total
        tax_amount = order.amount_tax

        # Prepare the ticket_data dictionary
        ticket_data = {
            'company_info': company_info,
            'order_name': order.name,
            'order_date': order.date_order,
            'order_lines': order_lines,
            'total_amount': total_amount,
            'tax_amount': tax_amount,
        }

        return ticket_data
