# -*- coding: utf-8 -*-

import serial
from odoo import models
import textwrap

class FP700Printer(models.AbstractModel):
    _name = 'fp700.printer'

    def send_data(self, data, printer_config):
        with serial.Serial(printer_config.serial_port, printer_config.baud_rate, timeout=1) as ser:
            ser.write(data)
            response = ser.read(64)
        return response

    def print_ticket(self, printer_config, ticket_data):
        # Implement ESC/POS commands to format and print the ticket
        data = self.prepare_esc_pos_commands(ticket_data)
        response = self.send_data(data, printer_config)
        return response

    def prepare_esc_pos_commands(self, ticket_data):
        # Helper function to format text
        def format_text(text, width, align='<'):
            return '{:{}{}}'.format(text, align, width)

        # ESC/POS commands
        cmds = []

        # Initialize printer
        cmds.append(b'\x1B\x40')  # Initialize printer

        # Print company information
        company_info = ticket_data['company_info']
        cmds.append(b'\x1B\x21\x08')  # Select double height font
        cmds.append(company_info['name'].encode())
        cmds.append(b'\x0A')  # Line feed

        cmds.append(b'\x1B\x21\x00')  # Select normal font
        address_parts = [
            company_info['address'],
            company_info['city'],
            f"{company_info['state']} {company_info['zip']}"
        ]
        for part in address_parts:
            cmds.append(part.encode())
            cmds.append(b'\x0A')  # Line feed

        cmds.append(f"Phone: {company_info['phone']}".encode())
        cmds.append(b'\x0A')  # Line feed
        cmds.append(f"VAT: {company_info['vat']}".encode())
        cmds.append(b'\x0A\x0A')  # Two line feeds

        # Print order details
        cmds.append(f"Order: {ticket_data['order_name']}".encode())
        cmds.append(b'\x0A')  # Line feed
        cmds.append(f"Date: {ticket_data['order_date']}".encode())
        cmds.append(b'\x0A\x0A')  # Two line feeds

        # Print order lines
        for line in ticket_data['order_lines']:
            product_name = textwrap.shorten(line['product_name'], width=20)
            qty = format_text(f"{line['quantity']}x", 4)
            price = format_text(f"{line['price']} ", 8, '>')
            line_text = f"{product_name} {qty} {price}"
            cmds.append(line_text.encode())
            cmds.append(b'\x0A')  # Line feed

        cmds.append(b'\x0A')  # Line feed

        # Print total and tax amounts
        cmds.append(b'\x1B\x21\x08')  # Select double height font
        cmds.append(f"Total: {ticket_data['total_amount']} ".encode())
        cmds.append(b'\x0A')  # Line feed
        cmds.append(b'\x1B\x21\x00')  # Select normal font
        cmds.append(f"Tax: {ticket_data['tax_amount']} ".encode())
        cmds.append(b'\x0A\x0A')  # Two line feeds

        # Cut the paper
        cmds.append(b'\x1D\x56\x00')  # Full cut

        # Concatenate commands and return
        return b''.join(cmds)
