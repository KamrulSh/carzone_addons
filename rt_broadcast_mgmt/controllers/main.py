from odoo import http
from odoo.http import request


class BookingSubmissionController(http.Controller):

    @http.route('/booking_form', type='http', auth='public', website=True)
    def booking_form(self, **kw):
        vehicle_brand_rec = request.env['fleet.vehicle.model.brand'].sudo().search([])
        vehicle_model_rec = request.env['fleet.vehicle.model'].sudo().search([])
        return request.render("rt_broadcast_mgmt.garage_booking_form",
                              {'vehicle_brand_rec': vehicle_brand_rec, 'vehicle_model_rec': vehicle_model_rec})

    @http.route('/create/booking', type="http", auth="public", website=True)
    def create_applicant(self, **kw):
        request.env['garage.booking'].sudo().create(kw)
        return request.render("rt_broadcast_mgmt.user_thanks", {})
