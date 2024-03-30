# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UniversityAdmission(models.Model):
    _name = 'admission.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Admission Register"
    _order = "name asc"
    _rec_name = 'name'

    name = fields.Char(string='Name', tracking=True)
    date_start = fields.Date(string='Start Date', tracking=True)
    date_end = fields.Date(string='End Date', tracking=True)
    course_id = fields.Many2one('university.course', string="Course")
    fees = fields.Float(string="Fees")
    max_no_of_regi = fields.Integer(string='Maximum No of Admission')
    min_no_of_regi = fields.Integer(string='Minimum No of Admission')
    academic_year = fields.Char(string='Academic Year')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'confirm'),
        ('gathering', 'application Gathering'),
        ('process', 'Admission Process'),
        ('done', 'Done')
    ], default='draft')

    registration_ids = fields.One2many('admission.registration', 'register_id', string="Registration")

    @api.constrains('date_start', 'date_end')
    def _check_registration(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                if rec.date_start > rec.date_end:
                    raise ValidationError("Date End Must be Greater Then Date Start")

    @api.constrains('min_no_of_regi', 'max_no_of_regi')
    def _check_registration(self):
        for rec in self:
            if rec.min_no_of_regi > 0 and rec.max_no_of_regi > 0:
                if rec.min_no_of_regi > rec.max_no_of_regi:
                    raise ValidationError("Maximum No of Admission Must be Greater Then Minimum No of Admission")

    @api.onchange('course_id')
    def onchange_course_id(self):
        for rec in self:
            rec.fees = rec.course_id.fees

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_gathering(self):
        for rec in self:
            rec.state = 'gathering'

    def action_process(self):
        for rec in self:
            rec.state = 'process'

    def action_done(self):
        for rec in self:
            rec.state = 'done'


class AdmissionRegistration(models.Model):
    _name = 'admission.registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Admission Registration"

    register_id = fields.Many2one('admission.register', string='Admission Register', tracking=True)
    name = fields.Char(string='Application_no', tracking=True)
    student_name = fields.Char(string='Student Name', tracking=True)
    pre = fields.Char(string="pre", compute='_compute_pre')
    mobile = fields.Char(string='Mobile', tracking=True)
    email = fields.Char(string='Email', tracking=True)
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
    discount = fields.Float(string="Discount")
    pre = fields.Char(string="pre", compute='_compute_pre')
    admission_date = fields.Date('Admission Date')
    application_date = fields.Date('Application Date')
    due_date = fields.Date('Due Date')
    is_student = fields.Boolean('Is Already Student')
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string='Batch')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], default='draft',
                             tracking=True)
    academic_year = fields.Char(string='Academic Year')
    fees = fields.Float(string="Fees")
    student_id = fields.Many2one('university.student', string='Student', tracking=True, copy=False)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_create_student(self):
        a_vals = []
        f_vals = []
        for rec in self:
            a_vals.append(((0, 0, {
                'course_id': rec.course_id.id,
                'batch_id': rec.batch_id.id,
            })))
            f_vals.append(((0, 0, {
                'date': rec.admission_date,
                'discount': rec.discount,
                'amount': rec.fees,
            })))
            student_id = self.env['university.student'].create({
                'name': rec.student_name,
                'email': rec.email,
                'mobile': rec.mobile,
                'date_of_birth': rec.date_of_birth,
                'gender': rec.gender,
                'blood_group': rec.blood_group,
                'visa_details': rec.visa_details,
                'country_id': rec.country_id.id,
                'state_id': rec.state_id.id,
                'course_id': rec.course_id.id,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'zip': rec.zip,
                'admission_ids': a_vals,
                'fees_ids': f_vals,
                # 'groups_id': [(6, 0, [self.ref('base.group_user')])]
            })
            rec.student_id = student_id


    def action_update_student(self):
        for rec in self:
            self.env['university.admission'].create({
                'student_id': rec.student_id.id,
                'course_id': rec.course_id.id,
                'batch_id': rec.batch_id.id,
            })

            self.env['student.fees'].create({
                'student_id': rec.student_id.id,
                'date': rec.admission_date,
                'discount': rec.discount,
                'amount': rec.fees,
            })
            rec.student_id.course_id = rec.course_id
            rec.student_id.email = rec.email
            rec.student_id.mobile = rec.mobile
            rec.student_id.date_of_birth = rec.date_of_birth
            rec.student_id.mobile = rec.mobile
            rec.student_id.email = rec.email
            rec.student_id.gender = rec.gender
            rec.student_id.blood_group = rec.blood_group
            rec.student_id.visa_details = rec.visa_details
            rec.student_id.country_id = rec.country_id
            rec.student_id.street = rec.street
            rec.student_id.street2 = rec.street2
            rec.student_id.city = rec.city
            rec.student_id.zip = rec.zip
            rec.student_id.state_id = rec.state_id

    @api.onchange('student_id')
    def onchange_student_id(self):
        for rec in self:
            rec.date_of_birth = rec.student_id.date_of_birth
            rec.mobile = rec.student_id.mobile
            rec.email = rec.student_id.email
            rec.gender = rec.student_id.gender
            rec.blood_group = rec.student_id.blood_group
            rec.visa_details = rec.student_id.visa_details
            rec.country_id = rec.student_id.country_id
            rec.street = rec.student_id.street
            rec.street2 = rec.student_id.street2
            rec.city = rec.student_id.city
            rec.zip = rec.student_id.zip
            rec.state_id = rec.student_id.state_id
            rec.student_name = rec.student_id.name

    @api.onchange('register_id')
    def onchange_register_id(self):
        for rec in self:
            rec.academic_year = rec.register_id.academic_year
            rec.course_id = rec.register_id.course_id
            rec.fees = rec.register_id.fees

    @api.depends('gender')
    def _compute_pre(self):
        for rec in self:
            if rec.gender == 'male':
                rec.pre = 'Mrs'
            elif rec.gender == 'female':
                rec.pre = 'Miss'
            else:
                rec.pre = ''

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('admission.registration') or 'New'
        return super(AdmissionRegistration, self).create(vals)
