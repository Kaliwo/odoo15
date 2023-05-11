from odoo import http
from odoo.http import request

class InternalUserAppointmentController(http.Controller):

    @http.route('/book_appointment', type='http', auth='user', website=True)
    def book_appointment(self, **kwargs):
        if not request.session.uid:
            return request.redirect('/web/login?redirect=/book_appointment')
        return request.render('website_portal_internal_users_appointment.appointment_template')
