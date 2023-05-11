from odoo import models, fields

class InternalUserAppointment(models.Model):
    _name = 'internal.user.appointment'
    _description = 'Internal User Appointment'

    user_id = fields.Many2one('res.users', string='User', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    description = fields.Text(string='Description')
