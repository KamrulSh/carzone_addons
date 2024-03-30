# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UniversityStudent(models.Model):
    _name = 'university.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Management"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('parents_name_uniq', 'unique (name,mobile,email,date_of_birth)', 'Student should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    pre = fields.Char(string="pre", compute='_compute_pre')
    mobile = fields.Char(string='Mobile', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    image = fields.Binary(string='Image', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    blood_group = fields.Char('Blood Group')
    visa_details = fields.Char('Visa Details')
    country_id = fields.Many2one('res.country', string="Country")
    street = fields.Char('Street1')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    zip = fields.Char('Pin Code')
    state_id = fields.Many2one('res.country.state', string="State")
    gr_no = fields.Char(string="GR Number")
    admission_ids = fields.One2many('university.admission', 'student_id', string="Admission")
    user_id = fields.Many2one('res.users', string="User")
    library_card_id = fields.Many2one('library.card', string="Library Card")
    library_ids = fields.One2many('student.library', 'student_id', string="Library")
    fees_ids = fields.One2many('student.fees', 'student_id', string="Library")
    registration_id = fields.Many2one('admission.registration', string='Application Registration')
    parent_id = fields.Many2one('student.parent', string='Parent')
    assignment_count = fields.Integer(compute='_compute_assignment_count', string='No of Assignment')

    activity_count = fields.Integer(compute='_compute_activity_count', string='No of Assignment')
    active = fields.Boolean('Active', default=True)
    course_id = fields.Many2one('university.course', string='Current Course')

    @api.model
    def create(self, vals):
        vals['gr_no'] = self.env['ir.sequence'].next_by_code('university.student') or 'New'
        return super(UniversityStudent, self).create(vals)


    def _compute_assignment_count(self):
        submission_obj = self.env['student.assignment']
        for rec in self:
            rec.assignment_count = submission_obj.search_count([('student_id', '=', rec.id)])

    def _compute_activity_count(self):
        submission_obj = self.env['mail.activity']
        for rec in self:
            rec.activity_count = submission_obj.search_count(
                [('res_id', '=', rec.id), ('res_model', '=', 'university.student')])

    def action_view_student_assignment(self):
        xml_id = 'university_management_odoo_app.student_assignment_view_tree'
        tree_view_id = self.env.ref(xml_id).id
        xml_id = 'university_management_odoo_app.student_assignment_view_form'
        form_view_id = self.env.ref(xml_id).id
        return {
            'name': 'Student Assignment',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(tree_view_id, 'tree'),
                      (form_view_id, 'form')],
            'res_model': 'student.assignment',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
            'type': 'ir.actions.act_window',
        }

    def action_view_student_activity(self):
        xml_id = 'mail.mail_activity_view_tree'
        tree_view_id = self.env.ref(xml_id).id
        xml_id = 'mail.mail_activity_view_form_popup'
        form_view_id = self.env.ref(xml_id).id
        return {
            'name': 'Student Activity',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(tree_view_id, 'tree'),
                      (form_view_id, 'form')],
            'res_model': 'mail.activity',
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'university.student')],
            'context': {'default_res_id': self.id, 'default_res_model': 'university.student'},
            'type': 'ir.actions.act_window',
        }

    @api.depends('gender')
    def _compute_pre(self):
        for rec in self:
            if rec.gender == 'male':
                rec.pre = 'Mrs'
            elif rec.gender == 'female':
                rec.pre = 'Miss'
            else:
                rec.pre = ''

    def action_create_user(self):
        for rec in self:
            if rec.email:
                user_id = self.env['res.users'].create({
                    'name': rec.name,
                    'login': rec.email,
                    # 'groups_id': [(6, 0, [self.ref('base.group_user')])]
                })
                rec.user_id = user_id
            else:
                raise ValidationError(
                    "Please Enter Email Address.")


class UniversityAdmission(models.Model):
    _name = 'university.admission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Admission"

    student_id = fields.Many2one('university.student', string='Student')
    course_id = fields.Many2one('university.course', string='Course')
    batch_id = fields.Many2one('university.batch', string='Batch')
    subject_id = fields.Many2one('university.subject', string='Subject')
    roll_no = fields.Char(string="Roll No")


class StudentLibrary(models.Model):
    _name = 'student.library'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Library"

    student_id = fields.Many2one('university.student', string='Student')
    faculty_id = fields.Many2one('university.faculty', string='Faculty')
    media_id = fields.Many2one('library.media', string="Media")
    unit_id = fields.Many2one('media.unit', string="Media Unit")
    issue_date = fields.Date(string='Issue Date', tracking=True)
    due_date = fields.Date(string='Due Date', tracking=True)
    type = fields.Selection([('student', 'Student'), ('faculty', 'Faculty')], default='student')
    return_date = fields.Date(string='Return Date', tracking=True)
    penalty = fields.Float(string="Penalty")
    library_card_id = fields.Many2one('library.card', string="Library Card")
    state = fields.Selection([('issue', 'Issue'), ('return', 'Return')], string='Status', tracking=True,
                             default='issue')

    @api.model
    def create(self, vals):
        print(vals['unit_id'], '-------------')
        unit_id = self.env['media.unit'].search([('id', '=', vals['unit_id'])])
        unit_id.state = 'issue'
        return super(StudentLibrary, self).create(vals)

    def action_return(self):
        for rec in self:
            rec.state = 'return'
            rec.unit_id.state = 'available'
            rec.return_date = date.today()


class StudentFees(models.Model):
    _name = 'student.fees'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Library"

    student_id = fields.Many2one('university.student', string='Student')
    invoice_id = fields.Many2one('account.move', string='Invoice No')
    date = fields.Date(string='Submit Date', tracking=True)
    amount = fields.Float(string="Amount")
    discount = fields.Float(string="Discount %")
    payable = fields.Float(string="Payable Amount", compute='compute_total_fees', store=True)
    status = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], default='draft', string='Status', tracking=True)

    @api.depends('amount', 'discount')
    def compute_total_fees(self):
        for rec in self:
            if rec.amount > 0 and rec.discount > 0:
                rec.payable = rec.amount - (rec.amount * rec.discount / 100)
            else:
                rec.payable = 0

    def action_create_invoice(self):
        invoice_lines=[]
        for rec in self:
            if rec.student_id.user_id:
                invoice_lines.append(((0, 0, {
                    'name': 'Student Fees',
                    # 'account_id': account_id.id,
                    'price_unit': rec.payable,
                    'quantity': 1,
                })))
                vals = {
                    'invoice_date': rec.date,
                    'move_type': 'out_invoice',
                    'state': 'draft',
                    'partner_id': rec.student_id.user_id.partner_id.id,
                    'invoice_line_ids': invoice_lines,
                }
                invoice_id = self.env['account.move'].create(vals)
                if invoice_id:
                    self.status = 'paid'
                    self.invoice_id = invoice_id
            else:
                raise ValidationError("First Create User Then after Invoice Created")
