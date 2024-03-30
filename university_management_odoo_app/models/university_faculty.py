# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UniversityFaculty(models.Model):
    _name = 'university.faculty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Faculty"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('parents_name_uniq', 'unique (name,mobile,email,date_of_birth)', 'Faculty should be unique.')
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
    subject_ids = fields.One2many('faculty.subject', 'faculty_id', string="Subject")
    user_id = fields.Many2one('res.users', string="User",copy=False)
    employee_id = fields.Many2one('hr.employee', string="Employee",copy=False)
    department_id = fields.Many2one('hr.department', string="Main Department")
    department_ids = fields.Many2many('hr.department', 'rel_faculty_department', 'faculty_id', 'department_id',
                                      string="Allocated Department")

    @api.depends('gender')
    def _compute_pre(self):
        for rec in self:
            if rec.gender == 'male':
                rec.pre = 'Mrs'
            elif rec.gender == 'female':
                rec.pre = 'Miss'
            else:
                rec.pre = ''

    def action_create_employee(self):
        for rec in self:
            if rec.email:
                employee_id = self.env['hr.employee'].create({
                    'name': rec.name,
                    'work_email': rec.email,
                    'mobile_phone': rec.mobile,
                    'gender': rec.gender,
                    'birthday': rec.date_of_birth,
                    'user_id': rec.user_id.id,
                    'department_id': rec.department_id.id,
                    'country_id': rec.country_id.id,
                    # 'groups_id': [(6, 0, [self.ref('base.group_user')])]
                })
                rec.employee_id = employee_id
                # if rec.user_id:
                #     rec.employee_id.user_id = rec.user_id
            else:
                raise ValidationError(
                    "Please Enter Email Address.")

    def action_create_user(self):
        for rec in self:
            if rec.email:
                user_id = self.env['res.users'].create({
                    'name': rec.name,
                    'login': rec.email,
                    # 'groups_id': [(6, 0, [self.ref('base.group_user')])]
                })
                rec.user_id = user_id
                if rec.employee_id:
                    rec.employee_id.user_id = user_id
            else:
                raise ValidationError(
                    "Please Enter Email Address.")


class FacultySubject(models.Model):
    _name = 'faculty.subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Faculty Subject"

    _sql_constraints = [
        ('faculty_subject_name_uniq', 'unique (subject_id,faculty_id)', 'Subject should be unique per Faculty.')
    ]

    faculty_id = fields.Many2one('university.faculty', string='Faculty')
    subject_id = fields.Many2one('university.subject', string='Subject')
    code = fields.Char(string='Code', tracking=True)
    type = fields.Selection([('theory', 'Theory'), ('practical', 'Practical')], string="Type")
    subject_type = fields.Selection([('compulsory', 'Compulsory'), ('optional', 'Optional')], string="Subject Type")
    grade = fields.Float(string="Grade Weightage")
    department_id = fields.Many2one('hr.department', string="Department")

    @api.onchange('faculty_id')
    def onchange_faculty_id(self):
        for rec in self:
            rec.department_id = rec.faculty_id.department_id

    @api.onchange('subject_id')
    def onchange_subject_id(self):
        for rec in self:
            if rec.subject_id:
                rec.code = rec.subject_id.code
                rec.type = rec.subject_id.type
                rec.subject_type = rec.subject_id.subject_type
                rec.grade = rec.subject_id.grade
                rec.department_id = rec.subject_id.department_id
