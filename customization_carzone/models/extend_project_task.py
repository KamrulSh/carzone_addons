import datetime

from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = "project.task"

    name = fields.Char(string="Name", required=False, related="number", store=True)
    cc_vehicle_in = fields.Date(string="Vehicle In", default=lambda self: fields.Date.context_today(self))
    cc_vehicle = fields.Many2one("fleet.vehicle", string="Vehicle",store=True, context="{'reg_no': True}", domain="['|', ('cc_partner', '=', partner_id),('cc_partner', '!=', False)]")

    @api.onchange('cc_vehicle')
    def onchange_cc_vehicle(self):
        for rec in self:
            if rec.cc_vehicle and rec.cc_vehicle.cc_partner:
                rec.partner_id = rec.cc_vehicle.cc_partner.id

    cc_partner_phone = fields.Char(string="Phone", related="partner_id.phone", store=True)
    cc_partner_mobile = fields.Char(string="Mobile", related="partner_id.mobile", store=True)
    cc_partner_email = fields.Char(string="Email", related="partner_id.email", store=True)
    cc_vehicle_make = fields.Many2one("fleet.vehicle.model.brand", related="cc_vehicle.cc_vehicle_make", string="Vehicle Make")
    cc_vehicle_model = fields.Many2one("fleet.vehicle.model", related="cc_vehicle.model_id", string="Vehicle Model")
    cc_vehicle_color = fields.Many2one("vehicle.color", related="cc_vehicle.cc_vehicle_color", string="Vehicle Color")
    register_no = fields.Char(string="Register No.", related="cc_vehicle.license_plate")
    vin = fields.Char(string="Register No.", related="cc_vehicle.vin_sn")
    engine = fields.Char(string="Engine No.", related="cc_vehicle.cc_engin_no")
    gear_nos = fields.Selection([('automatic','Automatic'),
                              ('manual','Manual')], string='Gear', related="cc_vehicle.cc_gears")
    year = fields.Char(string="Gears", related="cc_vehicle.cc_year")
    fuel_type = fields.Selection([
        ('petrol','Petrol'),
        ('diesel','Diesel'),
        ('gas','Gasoline'),
        ('electric', 'Electrical')
    ], string="Fuel Type", related="cc_vehicle.cc_fuel_type")
    type_id = fields.Many2one("vehicle.type.custom", string="Vehicle Type", related="cc_vehicle.cc_vehicle_type")
    cc_stage_id = fields.Selection([
        ('in','Vehicle In'),
        ('wip','Work in Progress'),
        ('hold','Hold'),
        ('no_action','No Action'),
        ('awaiting_parts','Waiting For Parts'),
        ('awaiting_approval','Waiting For Approval'),
        ('ready', 'Ready For Delivery'),
        ('delivered_not_invoiced', 'Delivered Not Invoiced'),
        ('road_testing', 'Road Testing'),
        ('washing', 'Washing'),
        ('out', 'Vehicle Out')
    ],default='in', track_visibility='always', string="Stage")

    def show_invoice(self):
        self.ensure_one()
        #        res = self.env.ref('account.action_invoice_tree1')
        res = self.env.ref('account.action_move_out_invoice_type')
        res = res.sudo().read()[0]
        res['domain'] = str([('cc_job_card', '=', self.id),('move_type', '=', 'out_invoice')])
        ###### fetch cost sheet lines for invoice line ids
        cost_sheet_line_ids = self.job_cost_sheet_ids
        if cost_sheet_line_ids:
            for line in cost_sheet_line_ids:
                lines = []
                vals = {
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'quantity': line.quantity,
                    'product_uom_id': line.product_id.uom_id.id,
                    'price_unit': line.cc_sale_price,
                    # 'sale_line_ids': [(6, 0, [line.id])],
                    'account_id': line.account_id.id,
                }
                lines.append((0, 0, vals))

        ###### fetch cost sheet lines for invoice line ids
        res['context'] = str({
                'default_cc_job_card': self.id,
                'default_move_type': 'out_invoice',
                'default_cc_vehicle': self.cc_vehicle.id if self.cc_vehicle else None,
                'default_partner_id': self.partner_id.id if self.partner_id else None,
                    })
        return res

    @api.depends('job_cost_sheet_ids.price_subtotal', 'custom_currency_id', 'company_id')
    def _compute_cost_sheet_amount(self):
        #        round_curr = self.custom_currency_id.round
        #        self.cost_sheet_amount_untaxed = sum(line.price_subtotal for line in self.job_cost_sheet_ids)
        #        self.cost_sheet_amount_tax = sum(round_curr(line.tax_amount) for line in self.job_cost_sheet_ids)
        #        self.cost_sheet_amount_total = self.cost_sheet_amount_untaxed + self.cost_sheet_amount_tax
        for rec in self:
            round_curr = rec.custom_currency_id.round
            rec.cost_sheet_amount_untaxed = sum((line.price_subtotal if line.cc_check_box else 0) for line in rec.job_cost_sheet_ids)
            rec.cost_sheet_amount_tax = sum(round_curr(line.tax_amount if line.cc_check_box else 0) for line in rec.job_cost_sheet_ids)
            rec.cost_sheet_amount_total = rec.cost_sheet_amount_untaxed + rec.cost_sheet_amount_tax

    def action_mrak_done(self):
        for rec in self:
            rec.is_close = True
            rec.cc_stage_id = 'ready'

    cc_color = fields.Integer(string="Color", compute="get_color", store=True)

    @api.depends('cc_stage_id')
    def get_color(self):
        for rec in self:
            if rec.cc_stage_id == 'wip':
                rec.cc_color = 1 # Deep Blue
            elif rec.cc_stage_id == 'hold':
                rec.cc_color = 2 #Yellow
            elif rec.cc_stage_id == 'awaiting_parts':
                rec.cc_color = 3 # Orange
            elif rec.cc_stage_id == 'awaiting_approval':
                rec.cc_color = 4 # Purple
            elif rec.cc_stage_id == 'ready':
                rec.cc_color = 5 # Deep Green
            elif rec.cc_stage_id == 'delivered_not_invoiced':
                rec.cc_color = 6 # red
            elif rec.cc_stage_id == 'out':
                rec.cc_color = 7 # Brown
            else:
                rec.cc_color = 0
