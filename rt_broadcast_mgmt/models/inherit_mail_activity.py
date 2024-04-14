from odoo import models, fields, api


class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = ['mail.activity', 'mail.thread']

    partner_id = fields.Many2one("res.partner", string="Customer", required=True, tracking=True)
    contact = fields.Char(related="partner_id.phone", string="Phone No.", tracking=True)
    email = fields.Char(related="partner_id.email", string="Email", tracking=True)
    planned_date = fields.Date(string="Planned Date", tracking=True)
    res_model_id = fields.Many2one('ir.model', 'Document Model', index=True, ondelete='cascade', required=True,
                                   default=lambda self: self.env.ref('rt_broadcast_mgmt.model_activity_general'))
    res_id = fields.Many2oneReference(string='Related Document ID', index=True, required=True, model_field='res_model',
                                      default=lambda self: self.env.ref('rt_broadcast_mgmt.general_activities'))
    whatsapp_data = fields.Html(string="Whatsapp Details", tracking=True)
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", string="Vehicle Model", tracking=True)
    vehicle_type = fields.Char(string="Vehicle Type", tracking=True)
    vehicle_color = fields.Char(string="Vehicle Color", tracking=True)
    engine_no = fields.Char(string="Engine No.", tracking=True)
    chassis_no = fields.Char(string="Chassis No.", tracking=True)
    license_plate = fields.Char(string="License Plate", tracking=True)
    last_odoo_meter_reading = fields.Char(string="Odoo meter reading", tracking=True)
    gear_type = fields.Char(string="Gear Type", tracking=True)
    fuel_type = fields.Char(string="Fuel Type", tracking=True)
    broadcasting_summary = fields.Text(tracking=True)
    date_deadline = fields.Date(tracking=True)

    @api.model
    def create(self, vals):
        res = super(MailActivity, self).create(vals)
        active_id = self.env.context.get('active_id')
        booking_mode = self.env.context.get('status')
        booking_id = self.env['garage.booking'].browse(active_id)
        if booking_mode == 'fleet':
            booking_id.write({
                'state': 'broadcast',
            })
        self.env['mail.message'].create(
            {'body': 'Broadcast data added.', 'message_type': 'comment',
             'model': 'garage.booking', 'res_id': active_id})
        return res

    # TODO: Need to modify for multiple vehicles for a single customer
    @api.onchange("partner_id")
    def onchange_partner_vehicle_data(self):
        partner_fleet = self.env['fleet.vehicle'].search([('cc_partner', '=', self.partner_id.id)])
        print(partner_fleet)
        if partner_fleet:
            for vehicle in partner_fleet:
                self.vehicle_model_id = vehicle.model_id.id
                self.vehicle_type = vehicle.cc_vehicle_type.name
                self.vehicle_color = vehicle.cc_vehicle_color.name
                self.engine_no = vehicle.cc_engin_no
                self.chassis_no = vehicle.vin_sn
                self.license_plate = vehicle.license_plate
                self.last_odoo_meter_reading = vehicle.odometer
                self.gear_type = vehicle.cc_gears
                self.fuel_type = vehicle.cc_fuel_type

        else:
            self.vehicle_model_id = False
            self.vehicle_type = False
            self.vehicle_color = False
            self.engine_no = False
            self.chassis_no = False
            self.license_plate = False
            self.last_odoo_meter_reading = False
            self.gear_type = False
            self.fuel_type = False

    @api.onchange("partner_id", "vehicle_model_id", "date_deadline", "planned_date", "activity_type_id")
    def onchange_whatsapp_data(self):
        company_name = self.env.company.name
        company_phone = self.env.company.phone
        for rec in self:
            whatsapp_template = self.env['broadcast.whatsapp.text'].search([], limit=1).text
            if whatsapp_template:
                formatted_whatsapp_data = whatsapp_template.format(
                    customer=rec.partner_id.name,
                    vehicle_model=rec.vehicle_model_id.name or '',
                    vehicle_type=rec.vehicle_type or '',
                    vehicle_color=rec.vehicle_color or '',
                    engine_no=rec.engine_no or '',
                    chassis_no=rec.chassis_no or '',
                    license_plate=rec.license_plate or '',
                    gear_type=rec.gear_type or '',
                    fuel_type=rec.fuel_type or '',
                    odoo_meter=rec.last_odoo_meter_reading or '',
                    due_date=str(rec.date_deadline) or '',
                    planned_date=str(rec.planned_date) or '',
                    company_name=company_name or '',
                    company_phone=company_phone or ''
                )
                rec.whatsapp_data = formatted_whatsapp_data
                rec.note = rec.whatsapp_data


class ActivityGeneral(models.Model):
    _name = 'activity.general'
    _description = 'Activity General'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')
