# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, fields


class Doctor(models.Model):
    """doctors and details"""
    _inherit = 'hr.employee'

    doc_seq = fields.Char(string='Doctor Sequence', required=True, copy=False,
                          readonly=True, index=True,
                          default=lambda self: 'New', help="Doctor Sequence")
    app_count = fields.Integer('Count', compute='_compute_count',
                               help="Total Appointment Count")

    def open_appointment(self):
        """Appointment  view"""
        return {
            'name': 'Appointment',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree',
            'context': {'create': False}
        }

    def _compute_count(self):
        """The no of appointments are calculated"""
        count = self.env['hospital.appointment'].search_count([(
            'doc_id', '=', self.name)])
        self.app_count = count
