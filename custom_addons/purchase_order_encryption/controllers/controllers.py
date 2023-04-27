# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderEncryption(http.Controller):
#     @http.route('/purchase_order_encryption/purchase_order_encryption', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_encryption/purchase_order_encryption/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_encryption.listing', {
#             'root': '/purchase_order_encryption/purchase_order_encryption',
#             'objects': http.request.env['purchase_order_encryption.purchase_order_encryption'].search([]),
#         })

#     @http.route('/purchase_order_encryption/purchase_order_encryption/objects/<model("purchase_order_encryption.purchase_order_encryption"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_encryption.object', {
#             'object': obj
#         })
