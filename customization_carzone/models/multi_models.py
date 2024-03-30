from odoo import models, fields, api

class VehicleColor(models.Model):
    _name = "vehicle.color"

    name = fields.Char(string="Vehicle Color")

class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    # cc_registration_no = fields.Char(string="Registration Number")
    cc_vehicle_make = fields.Many2one("fleet.vehicle.model.brand", related="model_id.brand_id", string="Vehicle Make")
    cc_vehicle_type = fields.Many2one("vehicle.type.custom", string="Vehicle Type")
    cc_vehicle_color = fields.Many2one("vehicle.color", string="Vehicle Color")
    # cc_vin = fields.Char(string="VIN")
    cc_engin_no = fields.Char(string="Engin No.")
    cc_gears = fields.Selection([('automatic','Automatic'),
                              ('manual','Manual')], string='Gears')
    cc_year = fields.Char(string="Year")
    cc_fuel_type = fields.Selection([
        ('petrol','Petrol'),
        ('diesel','Diesel'),
        ('gas','Gasoline'),
        ('electric', 'Electrical')
    ], string="Fuel Type")
    cc_partner = fields.Many2one("res.partner", string="Customer")
    cc_partner_phone = fields.Char(string="Phone", related="cc_partner.phone", store=True)
    cc_partner_email = fields.Char(string="Email", related="cc_partner.email", store=True)
    job_ids = fields.One2many("project.task", "cc_vehicle",string="Job IDS")
    count_job_ids = fields.Integer(string="Count Jobs", compute="_count_job_ids")

    @api.depends('job_ids')
    def _count_job_ids(self):
        for rec in self:
            rec.count_job_ids = len(rec.job_ids)

    def action_jobs_list(self):
        return {
            'name': ('Jobs'),
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('id', 'in', self.job_ids.ids)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    cc_account_move_ids = fields.One2many("account.move", "cc_vehicle", string="Account Move IDS")
    count_account_move_ids = fields.Integer(string="Count Jobs", compute="_count_account_move_ids")

    @api.depends('account_move_ids')
    def _count_account_move_ids(self):
        for rec in self:
            rec.count_account_move_ids = len(rec.cc_account_move_ids)

    def action_invoices_list(self):
        return {
            'name': ('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('id', 'in', self.cc_account_move_ids.ids)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }

    def name_get(self):
        result = []
        for rec in self:
            if self.env.context.get('reg_no'):
                name = rec.license_plate or "Empty"
                result.append((rec.id, name))
            else:
                name = rec.model_id.name + " [" + (rec.license_plate if rec.license_plate else "-") + "]"
                result.append((rec.id, name))
        return result

class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_ids = fields.One2many("fleet.vehicle", "cc_partner", string="Vehicle IDS")