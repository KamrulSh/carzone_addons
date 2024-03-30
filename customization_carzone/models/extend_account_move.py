from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class AccountMove(models.Model):
    _inherit = "account.move"

    cc_job_card = fields.Many2one("project.task", string="Job Card Number")
    cc_job_card_stage = fields.Selection([
        ('in','Vehicle In'),
        ('wip','Work in Progress'),
        ('hold','Hold'),
        ('no_action','No Action'),
        ('awaiting_parts','Waiting For Parts'),
        ('awaiting_approval','Waiting For Approval'),
        ('ready', 'Ready For Delivery'),
        ('delivered_not_invoiced', 'Delivered Not Invoiced'),
        ('out', 'Vehicle Out')
    ], string="Stage", related="cc_job_card.cc_stage_id", store=True)
    cc_vehicle = fields.Many2one("fleet.vehicle",string="Vehicle")
    cc_registration_no = fields.Char(string="Registration Number", related="cc_vehicle.license_plate")
    cc_vehicle_make = fields.Many2one("fleet.vehicle.model.brand", related="cc_vehicle.cc_vehicle_make", string="Vehicle Make")
    cc_vehicle_model = fields.Many2one("fleet.vehicle.model", related="cc_vehicle.model_id", string="Vehicle Model")
    cc_vehicle_type = fields.Many2one("vehicle.type.custom", string="Vehicle Type", related="cc_vehicle.cc_vehicle_type")
    cc_vehicle_color = fields.Many2one("vehicle.color", related="cc_vehicle.cc_vehicle_color", string="Vehicle Color")
    cc_vin = fields.Char(string="VIN", related="cc_vehicle.vin_sn")
    cc_engin_no = fields.Char(string="Engin No.", related="cc_vehicle.cc_engin_no")
    cc_gears = fields.Selection([('automatic','Automatic'),
                              ('manual','Manual')], string='Gears', related="cc_vehicle.cc_gears")
    cc_year = fields.Char(string="Year", related="cc_vehicle.cc_year")
    cc_fuel_type = fields.Selection([
        ('petrol','Petrol'),
        ('diesel','Diesel'),
        ('gas','Gasoline'),
        ('electric', 'Electrical')
    ], string="Fuel Type", related="cc_vehicle.cc_fuel_type")
    cc_complaints = fields.Html(string="Complaints")

    @api.onchange('cc_job_card')
    def _onchange_cc_job_card(self):
        for rec in self:
            job_card_id = rec.cc_job_card
            if job_card_id:
                rec.task_id = job_card_id.id
                cost_sheet_line_ids = job_card_id.job_cost_sheet_ids
                if job_card_id.cc_vehicle:
                    rec.cc_vehicle = rec.cc_job_card.cc_vehicle.id
                if job_card_id.description:
                    rec.cc_complaints = rec.cc_job_card.description
                if rec.move_type == "out_invoice":
                    if job_card_id.partner_id:
                        rec.partner_id = job_card_id.partner_id.id
                    if cost_sheet_line_ids:
                        rec.invoice_line_ids = [(5,0,0)]  # Clear existing invoice lines
                        rec.line_ids = [(5,0,0)]  # Clear existing lines
                        # sum = 0.0
                        for line in cost_sheet_line_ids:
                            lines = []
                            if line.cc_check_box:
                                # sum += line.quantity * line.price_unit
                                vals = {
                                    'product_id': line.product_id.id,
                                    'name': line.product_id.name,
                                    'quantity': line.quantity,
                                    'product_uom_id': line.product_id.uom_id.id,
                                    # 'price_unit': line.cc_sale_price if line.cost_type == 'sublet' else line.price_unit,
                                    'price_unit': line.cc_sale_price if line.cc_sale_price else line.price_unit,
                                    # 'sale_line_ids': [(6, 0, [line.id])],
                                    'account_id': line.account_id.id,
                                    'currency_id': self.env.user.company_id.currency_id,
                                    'tax_ids': line.invoice_line_tax_ids,
                                    'move_id': rec.id,
                                }
                                lines.append((0, 0, vals))
                            # rec.invoice_line_ids = lines
                            # rec.line_ids = [(5, 0, 0)]
                            # rec = rec.with_context(check_move_validity=False)
                            # rec.update({'invoice_line_ids': lines})
                            rec.invoice_line_ids = lines
                            rec._onchange_partner_id()
                            #rec.line_ids._onchange_product_id()
                            rec.line_ids._onchange_account_id()
                            rec.line_ids._onchange_price_subtotal()
                            rec._recompute_dynamic_lines(
                                recompute_all_taxes=True,
                                recompute_tax_base_amount=True,
                            )

    # def write(self, vals):
        # excess_amount = self.excess_amount
        # invoice_date = self.invoice_date
        # if not invoice_date:
        #     raise ValidationError("Please Select Invoice Date First!")
        # if not excess_amount:
        #     invoice_line_ids = vals.get('invoice_line_ids')
        #     if invoice_line_ids != None:
        #         if len(invoice_line_ids) != len(self.invoice_line_ids):
        #             if 'line_ids' in vals:
        #                 del vals['line_ids']
        # rtn = super(AccountMove, self).write(vals)
        # vals['invoice_date'] = datetime.date.today()
        # return rtn

    # @api.model_create_multi
    # def create(self, vals_list):
        # excess_amount = vals_list[0]['excess_amount']
        # if not excess_amount:
        #     if type(vals_list) == list:
        #         for val in vals_list:
        #             invoice_line_ids = val.get('invoice_line_ids')
        #             if invoice_line_ids != None:
        #                 if len(invoice_line_ids) != len(self.invoice_line_ids):
        #                     del val['line_ids']
        #     else:
        #         invoice_line_ids = vals_list.get('invoice_line_ids')
        #         if invoice_line_ids != None:
        #             if len(invoice_line_ids) != len(self.invoice_line_ids):
        #                 del vals_list['line_ids']

        # vals = super(AccountMove, self).create(vals_list)
        # invoice_date = vals['invoice_date']
        # if not invoice_date:
        #     raise ValidationError("Please Select Invoice Date First!")
        # return vals

    def create_gatepass(self):
        for rec in self:
            job_card = rec.cc_job_card
            if job_card:
                job_card.cc_stage_id = 'out'
                job_card.date_end = datetime.datetime.now()

    def print_gatepass(self):
        pass

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    cc_sale_price = fields.Float(string="Sale Price")
    cc_cost_type = fields.Selection(
        [('material', 'Material'),
         ('overhead', 'Overhead'),
         ('labour', 'Labour'),
         ('sublet', 'Sublet')
         ],
        string='Type',
        default='material',
    )


    def create(self, vals_list):
        rtn = super(AccountMoveLine, self).create(vals_list)
        for rec in rtn:
            if rec.move_id.move_type in ['in_invoice'] and rec.move_id.cc_job_card and rec.product_id:
                job_card = rec.move_id.cc_job_card
                job_cost_sheet = self.env['job.cost.sheet']
                job_cost_sheet_exists = job_cost_sheet.search([('cc_account_move_line_id', '=', rec.id)])

                if job_cost_sheet_exists:
                    for line in job_cost_sheet_exists:
                        line.write({
                            'cost_type': rec.cc_cost_type,
                            'product_id': rec.product_id.id,
                            'account_id': rec.account_id.id,
                            'account_analytic_id': rec.analytic_account_id.id if rec.analytic_account_id else "",
                            'quantity': rec.quantity,
                            'uom_id': rec.product_uom_id.id,
                            'cc_sale_price': rec.cc_sale_price,
                            'price_unit': rec.cc_sale_price if rec.cc_sale_price else rec.price_unit,
                            'discount': rec.discount,
                            'invoice_line_tax_ids': rec.tax_ids,
                            'price_subtotal': rec.price_subtotal,
                            'task_id': job_card.id,
                            'cc_account_move_line_id': rec.id,
                            'name': rec.name or rec.product_id.name,
                            'cc_check_box': True
                        })
                else:
                    job_cost_sheet.create({
                        'cost_type': rec.cc_cost_type,
                        'product_id': rec.product_id.id,
                        'account_id': rec.account_id.id,
                        'account_analytic_id': rec.analytic_account_id.id if rec.analytic_account_id else None,
                        'quantity': rec.quantity,
                        'uom_id': rec.product_uom_id.id,
                        'cc_sale_price': rec.cc_sale_price,
                        'price_unit': rec.cc_sale_price if rec.cc_sale_price else rec.price_unit,
                        'discount': rec.discount,
                        'invoice_line_tax_ids': rec.tax_ids,
                        'price_subtotal': rec.price_subtotal,
                        'task_id': rec.move_id.cc_job_card.id,
                        'cc_account_move_line_id': rec.id,
                        'name': rec.name or rec.product_id.name,
                        'cc_check_box': True

                    })
        return rtn

    def write(self, vals_list):
        rtn = super(AccountMoveLine, self).write(vals_list)
        for rec in self:
            if rec.move_id.move_type in ['in_invoice'] and rec.move_id.cc_job_card and rec.product_id:
                job_card = rec.move_id.cc_job_card
                job_cost_sheet = self.env['job.cost.sheet']
                job_cost_sheet_exists = job_cost_sheet.search([('cc_account_move_line_id', '=', rec.id)])

                if job_cost_sheet_exists:
                    for line in job_cost_sheet_exists:
                        line.write({
                            'cost_type': rec.cc_cost_type,
                            'product_id': rec.product_id.id,
                            'account_id': rec.account_id.id,
                            'account_analytic_id': rec.analytic_account_id.id if rec.analytic_account_id else None,
                            'quantity': rec.quantity,
                            'uom_id': rec.product_uom_id.id,
                            'cc_sale_price': rec.cc_sale_price,
                            'price_unit': rec.cc_sale_price if rec.cc_sale_price else rec.price_unit,
                            'discount': rec.discount,
                            'invoice_line_tax_ids': rec.tax_ids,
                            'price_subtotal': rec.price_subtotal,
                            'task_id': job_card.id,
                            'cc_account_move_line_id': rec.id,
                            'name': rec.name or rec.product_id.name
                        })
                else:
                    job_cost_sheet.create({
                        'cost_type': rec.cc_cost_type,
                        'product_id': rec.product_id.id,
                        'account_id': rec.account_id.id,
                        'account_analytic_id': rec.analytic_account_id.id if rec.analytic_account_id else "",
                        'quantity': rec.quantity,
                        'uom_id': rec.product_uom_id.id,
                        'cc_sale_price': rec.cc_sale_price,
                        'price_unit': rec.cc_sale_price if rec.cc_sale_price else rec.price_unit,
                        'discount': rec.discount,
                        'invoice_line_tax_ids': rec.tax_ids,
                        'price_subtotal': rec.price_subtotal,
                        'task_id': rec.move_id.cc_job_card.id,
                        'cc_account_move_line_id': rec.id,
                        'name': rec.name or rec.product_id.name

                    })
        return rtn
