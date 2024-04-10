from odoo import models, fields, api


class WhatsappText(models.Model):
    _name = "broadcast.whatsapp.text"
    _description = "Whatsapp Text"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", default="Whatsapp text")
    text = fields.Html(string="Whatsapp Text", store=True, required=True)

    @api.onchange("text")
    def onchange_whatsapp_text(self):
        company_name = self.env.company.name
        company_phone = self.env.company.phone

        broadcasts = self.env['mail.activity'].search([])
        for broadcast in broadcasts:
            whatsapp_template = self.text
            if whatsapp_template:
                formatted_whatsapp_data = whatsapp_template.format(
                    customer=broadcast.partner_id.name,
                    vehicle_model=broadcast.vehicle_model_id.name or '',
                    vehicle_type=broadcast.vehicle_type or '',
                    vehicle_color=broadcast.vehicle_color or '',
                    engine_no=broadcast.engine_no or '',
                    chassis_no=broadcast.chassis_no or '',
                    license_plate=broadcast.license_plate or '',
                    gear_type=broadcast.gear_type or '',
                    fuel_type=broadcast.fuel_type or '',
                    odoo_meter=broadcast.last_odoo_meter_reading or '',
                    due_date=str(broadcast.date_deadline) or '',
                    planned_date=str(broadcast.planned_date) or '',
                    company_name=company_name or '',
                    company_phone=company_phone or ''
                )
                broadcast.whatsapp_data = formatted_whatsapp_data
