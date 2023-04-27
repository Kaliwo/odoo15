from addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class PatientPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):

        rtn = super(PatientPortal, self)._prepare_home_portal_values(counters)

        rtn['prescriptions_counts'] = request.env['base_hospital_management.prescription'].search_count([])
        return rtn
