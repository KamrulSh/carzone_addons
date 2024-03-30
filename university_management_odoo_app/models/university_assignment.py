# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UniversityAssignment(models.Model):
    _name = 'university.assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Assignment"
    _order = "name asc"
    _rec_name = 'name'

    name = fields.Char(string='Name', tracking=True)
    course_id = fields.Many2one('university.course', string="Course", tracking=True)
    batch_id = fields.Many2one('university.batch', string='Batch', tracking=True)
    subject_id = fields.Many2one('university.subject', string='Subject', tracking=True)
    faculty_id = fields.Many2one('university.faculty', string='Faculty', tracking=True)
    assignment_type_id = fields.Many2one('assignment.type', string='Assignment Type', tracking=True)
    reviewer = fields.Char(string="Reviewer")
    issue_date = fields.Date(string="Issue Date", tracking=True)
    submission_date = fields.Date(string="Submission Date", tracking=True)
    marks = fields.Float(string="Marks", tracking=True)
    remarks = fields.Text(string="Remarks")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'confirm'),
        ('done', 'Done')
    ], default='draft')

    submission_ids = fields.One2many('student.assignment', 'assignment_id', string="Student Assignment")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('university.assignment') or 'New'
        return super(UniversityAssignment, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'


class StudentAssignment(models.Model):
    _name = 'student.assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Assignment"
    _rec_name = 'assignment_id'

    _sql_constraints = [
        ('student_assignment_uniq', 'unique (student_id,assignment_id)', 'Student should be unique per Assignment.')
    ]

    assignment_id = fields.Many2one('university.assignment', string='Assignment', tracking=True)
    marks = fields.Float(string="Marks")
    submission_date = fields.Date('Application Date')
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('accepted', 'Accepted')],
                             default='draft',
                             tracking=True)
    student_id = fields.Many2one('university.student', string='Student', tracking=True)
    remarks = fields.Text(string="Remarks")
    note = fields.Text(string="Note")
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.onchange('assignment_id')
    def onchange_assignment_id(self):
        for rec in self:
            rec.course_id = rec.assignment_id.course_id
            rec.batch_id = rec.assignment_id.batch_id

    def action_submitted(self):
        for rec in self:
            rec.state = 'submitted'

    def action_accepted(self):
        for rec in self:
            rec.state = 'accepted'


