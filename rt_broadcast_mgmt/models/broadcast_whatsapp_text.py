from odoo import models, fields, api


class WhatsappText(models.Model):
    _name = "broadcast.whatsapp.text"
    _description = "Whatsapp Text"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", default="Whatsapp text")
    text = fields.Html(string="Whatsapp Text", store=True, required=True)

    @api.onchange("text")
    def onchange_whatsapp_text(self):
        """
        On change of whatsapp master text in Configuration,
        updated text will reflect in whatsapp text box of
        each broadcasting record.
        """
        company_name = self.env.company.name
        company_phone = self.env.company.phone

        broadcasts = self.env['mail.activity'].search([])
        for rec in broadcasts:
            rec.whatsapp_data = self.text
            if rec.whatsapp_data:
                rec.whatsapp_data = rec.whatsapp_data % {'customer': rec.partner_id.name,
                                                         'vehicle_model': rec.vehicle_model_id.name,
                                                         'vehicle_type': rec.vehicle_type,
                                                         'vehicle_color': rec.vehicle_color,
                                                         'engine_no': rec.engine_no,
                                                         'chassis_no': rec.chassis_no,
                                                         'license_plate': rec.license_plate,
                                                         'gear_type': rec.gear_type,
                                                         'fuel_type': rec.fuel_type,
                                                         'odoo_meter': rec.last_odoo_meter_reading,
                                                         'due_date': str(rec.date_deadline),
                                                         'planned_date': str(rec.planned_date),
                                                         'company_name': company_name,
                                                         'company_phone': company_phone}
