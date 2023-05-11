from odoo import http
from odoo.http import request

class WebsitePortalInternalUsers(http.Controller):

    @http.route('/internal_users', type='http', auth='public', website=True)
    def internal_users(self, **kw):
        users = request.env['res.users'].sudo().search([('share', '=', False)])
        return request.render('website_portal_internal_users.internal_users', {'users': users})

    @http.route('/vendor_list', type='http', auth='public', website=True)
    def vendor_list(self, **kw):
        vendors = request.env['res.partner'].sudo().search([('supplier_rank', '>', 0)])
        return request.render('website_portal_internal_users.vendor_list', {'vendors': vendors})
