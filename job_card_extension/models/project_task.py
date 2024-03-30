# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models

def get_current_time():
    """
    Return current time
    """
    current_time = datetime.now().time()
    hours = current_time.hour
    minutes = current_time.minute
    time_in_float = float(str(hours) + "." + str(minutes))
    return time_in_float

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # job_no = fields.Char(string="Job No", compute="compute_job_no", store=True)
    num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    condition = fields.Text(string="Terms & Condition")
    warranty = fields.Many2one("job.card.warranty", string="Warranty")
    title = fields.Selection([('mr', 'Mr.'), ('mrs', 'Mrs.'), ('miss', 'Miss')])
    quality_checklist_ids = fields.Many2many('quality.checklist', 'job_card_id', string="Quality Checklist")

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.custom_currency_id.amount_to_text(round(rec.cost_sheet_amount_total))) + ' only'


    def separate_cost_sheet_lines(self):
        """
        Separate cost sheet lines
        """
        job_cost_sheet_list = []

        for rec in self:
            if rec.job_cost_sheet_ids:
                for type in sorted(set(rec.job_cost_sheet_ids.mapped('cost_type'))):
                    cost_sheet_list = []
                    cost_sheet_list.append(rec.job_cost_sheet_ids.filtered(lambda x: x.cost_type == type))
                    job_cost_sheet_list.append(cost_sheet_list)
        return job_cost_sheet_list

class JobCostSheet(models.Model):
    _inherit = "job.cost.sheet"

    def create(self, vals):
        if type(vals) == list:
            for val in vals:
                if val.get("cc_sale_price"):
                    val["price_unit"] = val.get("cc_sale_price")
        else:
            if vals.get("cc_sale_price"):
                vals["price_unit"] = vals.get("cc_sale_price")
        return super(JobCostSheet, self).create(vals)

    def write(self, vals):
        if vals.get("cc_sale_price"):
            self.price_unit = vals.get("cc_sale_price")
        res = super(JobCostSheet, self).write(vals)
        # self.price_unit = self.cc_sale_price if self.cc_sale_price else self.price_unit
        return res

class AccountMove(models.Model):
    _inherit = "account.move"

    def separate_invoice_lines(self):
        """
        Separate invoice lines
        """
        invoice_cost_sheet_list = []

        for rec in self:
            if rec.invoice_line_ids:
                for cost_type in sorted(set(rec.invoice_line_ids.mapped('cc_cost_type'))):
                    cost_sheet_list = []
                    cost_sheet_list.append(rec.invoice_line_ids.filtered(lambda x: x.cc_cost_type == cost_type))
                    invoice_cost_sheet_list.append(cost_sheet_list)
        return invoice_cost_sheet_list

class JobCardStage(models.Model):
    _name = "job.card.stage"

    name = fields.Char(string="Name")
    value = fields.Char(string="Value")
    color = fields.Char(string="Color")
    project_task_id = fields.Many2one("project.task", string="Job Card")
    count_vehicle_in = fields.Integer(string="Vehicle In Count", compute="compute_stage_records")
    count_work_in_progress = fields.Integer(string="Work In Progress Count", compute="compute_stage_records")
    count_hold = fields.Integer(string="Hold Count", compute="compute_stage_records")
    count_no_action = fields.Integer(string="No Action Count", compute="compute_stage_records")
    count_awaiting_parts = fields.Integer(string="Waiting for Parts Count", compute="compute_stage_records")
    count_awaiting_approval = fields.Integer(string="Waiting for Approval Count", compute="compute_stage_records")
    count_ready = fields.Integer(string="Ready for Delivery Count", compute="compute_stage_records")
    count_delivered_not_invoiced = fields.Integer(string="Delivered not Invoiced Count", compute="compute_stage_records")
    count_out = fields.Integer(string="Vehicle Out Count", compute="compute_stage_records")
    count_road_testing = fields.Integer(string="Road Testing Count", compute="compute_stage_records")
    count_washing = fields.Integer(string="Washing Count", compute="compute_stage_records")
    count_total = fields.Integer(string="Total Count", compute="compute_stage_records")

    def compute_stage_records(self):
        """
        Compute job card having state of Vehicle In
        """
        self.count_vehicle_in = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'in')])
        self.count_work_in_progress = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'wip')])
        self.count_hold = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'hold')])
        self.count_no_action = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'no_action')])
        self.count_awaiting_parts = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'awaiting_parts')])
        self.count_awaiting_approval = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'awaiting_approval')])
        self.count_ready = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'ready')])
        self.count_delivered_not_invoiced = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'delivered_not_invoiced')])
        self.count_out = self.env['project.task'].search_count([('is_jobcard', '=', True), ('cc_stage_id', '=', 'out'), ('date_end', '>=', fields.Datetime.now().replace(hour=0, minute=0, second=0)),
                       ('date_end', '<=', fields.Datetime.now().replace(hour=23, minute=59, second=59))])
        self.count_road_testing = self.env['project.task'].search_count(
            [('is_jobcard', '=', True), ('cc_stage_id', '=', 'road_testing')])
        self.count_washing = self.env['project.task'].search_count(
            [('is_jobcard', '=', True), ('cc_stage_id', '=', 'washing')])
        self.count_total = self.env['project.task'].search_count([('is_jobcard', '=', True)])

    def get_action_job_card_ready(self):
        """
        Get action of job card
        """
        action_obj = self.env["ir.actions.actions"]
        # Vehicle In
        if self.value == 'in':
            action = action_obj._for_xml_id('job_card_extension.open_vehicle_in_job_card')
        
        # Work In Progress
        if self.value == 'wip':
            action = action_obj._for_xml_id('job_card_extension.open_work_in_progress_job_card')
            
        # Hold
        if self.value == 'hold':
            action = action_obj._for_xml_id('job_card_extension.open_hold_job_card')
        
        # No Action
        if self.value == 'no_action':
            action = action_obj._for_xml_id('job_card_extension.open_no_action_job_card')
            
        # Waiting For Parts
        if self.value == 'awaiting_parts':
            action = action_obj._for_xml_id('job_card_extension.open_awaiting_parts_job_card')
        
        # Waiting For Approval
        if self.value == 'awaiting_approval':
            action = action_obj._for_xml_id('job_card_extension.open_awaiting_approval_job_card')
        
        # Ready For Delivery
        if self.value == 'ready':
            action = action_obj._for_xml_id('job_card_extension.open_ready_job_card')
        
        # Delivered Not Invoiced
        if self.value == 'delivered_not_invoiced':
            action = action_obj._for_xml_id('job_card_extension.open_delivered_not_invoiced_job_card')
        
        # Vehicle Out
        if self.value == 'out':
            action = action_obj._for_xml_id('job_card_extension.open_out_job_card')
            action['domain'] = [('is_jobcard', '=', True), ('cc_stage_id', '=', 'out'), ('date_end', '>=', fields.Datetime.now().replace(hour=0, minute=0, second=0)),
                       ('date_end', '<=', fields.Datetime.now().replace(hour=23, minute=59, second=59))]

        # Road Testing
        if self.value == 'road_testing':
            action = action_obj._for_xml_id('job_card_extension.open_road_testing_job_card')

        # Washing
        if self.value == 'washing':
            action = action_obj._for_xml_id('job_card_extension.open_washing_job_card')

        # Total
        if self.value == 'total':
            action = action_obj._for_xml_id('job_card_extension.open_total_job_card')
            
        if action:
            return action
        return True

class JobCardWarranty(models.Model):
    _name = "job.card.warranty"

    name = fields.Char(string="Name")
class InstructionJobOrder(models.Model):
    _inherit = "instruction.job.order"

    assign_hours = fields.Float(string="Assign Hours", digits=(16, 2))
    total_hours = fields.Float(string="Total Hours", digits=(16, 2))
    job_card_payment_id = fields.Many2one('job.card.payment', string="Categories")
    task_planned_hours = fields.Float(string="Task Planned Hours", compute="compute_task_planned_hours", store=True)

    @api.depends('assign_hours')
    def compute_task_planned_hours(self):
        """
        Compute planned hours
        """
        total_planned_hours = 0.0
        for rec in self:
            if rec.assign_hours:
                total_planned_hours += rec.assign_hours
            rec.task_planned_hours = total_planned_hours
            rec.task_id.planned_hours = total_planned_hours

    def create(self, vals):
        res = super(InstructionJobOrder, self).create(vals)
        timesheet = self.env['account.analytic.line'].create({
            'instruction_job_id': res.id,
            'description': res.description,
            'name': res.note,
            'user_id': res.user_id.id,
            'job_card_payment_id': res. job_card_payment_id.id,
            'assign_hours': res.assign_hours,
            'account_id': res.task_id.analytic_account_id.id,
            'task_id': res.task_id.id,
            # 'start_time': get_current_time()
        })
        timesheet.flush()
        return res

    def write(self, vals):
        res = super(InstructionJobOrder, self).write(vals)

        if any( key in vals for key in ('description', 'name',
                                        'user_id',
                                        'job_card_payment_id',
                                        'assign_hours')):
            timesheet_id = self.env['account.analytic.line'].search(
                [('instruction_job_id', '=', self.id)]
            )
            if timesheet_id:
                timesheet_id.write(vals)

        return res

    def unlink(self):
        timesheet_id = self.env['account.analytic.line'].search(
            [('instruction_job_id', '=', self.id)]
        )
        if timesheet_id:
            timesheet_id.unlink()
        return super(InstructionJobOrder, self).unlink()

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    user_id = fields.Many2one(
        'res.users',
        string="User",
        default=lambda self: self.env.user.id,
        readonly=True,
    )
    job_card_payment_id = fields.Many2one('job.card.payment', string="Categories")
    assign_hours = fields.Float(string="Assign Hours", digits=(16, 2))
    start_time = fields.Float(string="Start Time", digits=(16, 2))
    end_time = fields.Float(string="End Time", digits=(16, 2))
    is_start_time = fields.Boolean(string="Is start time?")
    is_end_time = fields.Boolean(string="Is start time?")
    total_hours = fields.Float(string="Total hours", compute="compute_total_hours", store=True)
    employees_id = fields.Many2one(
        'hr.employee',
        string="Technician",
        required=False,
        domain="[('department_id', '=', departments_id)]"
    )
    employee_user_id = fields.Many2one(related="employees_id.user_id", string="Employee User")
    departments_id = fields.Many2one('hr.department', "Department")
    vehicle_id = fields.Many2one(related='task_id.cc_vehicle', string="Vehicle", store=True)
    vehicle_model_id = fields.Many2one(related='task_id.cc_vehicle_model', string="Vehicle Model", store=True)

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.instruction_job_id:
                timesheet_ids = self.search([('instruction_job_id', '=', rec.instruction_job_id.id)])
                instruction_id = self.env['instruction.job.order'].search([('id', '=', rec.instruction_job_id.id)])
                total_hours = 0.0
                if instruction_id:
                    for timesheet in timesheet_ids:
                        total_hours += timesheet.unit_amount
                    instruction_id.total_hours = total_hours

        return res

    def action_start_time(self):
        """
        Action to add start time
        """
        if not self.is_start_time:
            self.start_time = get_current_time()
            self.is_start_time = True

    def action_end_time(self):
        """
        Action to add start time
        """
        if not self.is_end_time:
            self.end_time = get_current_time()
            self.is_end_time = True

    @api.depends('start_time', 'end_time')
    def compute_total_hours(self):
        """
        On change end time
        """
        for rec in self:
            if rec.start_time and rec.end_time:
                total_time = 0.0
                total_time = rec.start_time + rec.end_time
                rec.unit_amount = total_time
                rec.total_hours = total_time

class QualityChecklist(models.Model):
    _inherit = "quality.checklist"

    job_card_id = fields.Many2one('project.task', string="Job Card")
    qc_image = fields.Binary(string="Image")



