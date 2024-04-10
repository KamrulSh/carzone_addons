from odoo import models, fields, api


class WhatsappText(models.Model):
    _name = "booking.whatsapp.text"
    _description = "Booking Whatsapp Text"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", default="Whatsapp text")
    text = fields.Html(string="Whatsapp Text", store=True, required=True)

    @api.onchange("text")
    def onchange_booking_whatsapp_text(self):
        company_name = self.env.company.name
        company_phone = self.env.company.phone

        bookings = self.env["garage.booking"].search([])
        for booking in bookings:
            whatsapp_template = self.text
            if whatsapp_template:
                formatted_whatsapp_data = whatsapp_template.format(
                    customer_name=booking.customer_name or '',
                    customer_email=booking.customer_email or '',
                    customer_phone=booking.customer_phone or '',
                    booking_date=str(booking.booking_date) or '',
                    date_deadline=str(booking.date_deadline) or '',
                    planned_date=str(booking.planned_date) or '',
                    license_plate=booking.vehicle_no or '',
                    vehicle_model=booking.vehicle_model_id.name or '',
                    chassis_no=booking.chassis_no or '',
                    company_name=company_name or '',
                    company_phone=company_phone or '',
                )
                booking.whatsapp_data = formatted_whatsapp_data
