from odoo import http
from odoo.http import request


class BookingSubmissionController(http.Controller):

    @http.route('/booking_form', type='http', auth='public', website=True)
    def booking_form(self, **kw):
        return request.render("rt_broadcast_mgmt.garage_booking_form", {})

    @http.route('/create/booking', type="http", auth="public", website=True)
    def create_applicant(self, **kw):
        request.env['garage.booking'].sudo().create(kw)
        return request.render("rt_broadcast_mgmt.user_thanks", {})
