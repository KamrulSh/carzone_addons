# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentMarksheet(models.Model):
    _name = 'student.marksheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Session"
    _rec_name = 'name'

    _sql_constraints = [
        ('result_template_name_uniq', 'unique (name,result_template_id)', 'Marksheet should be unique for per result template.')
    ]

    name = fields.Char(string='Marksheet', tracking=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    total_pass = fields.Integer(string='Total Pass', tracking=True, compute='compute_total_result', store=True)
    total_fail = fields.Integer(string='Total Fail', tracking=True, compute='compute_total_result', store=True)
    result_template_id = fields.Many2one('result.template', string="Result Template")
    session_id = fields.Many2one('university.exam', string='Exam Session', tracking=True)
    date = fields.Date(string="Generated Date")
    line_ids = fields.One2many('student.marksheet.line', 'marksheet_id', string="Subject")
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('cancel', 'Cancel')],
                             default='draft', tracking=True)
    pass_mark = fields.Float(string='Passing Marks')

    @api.onchange('result_template_id')
    def onchange_result_template_id(self):
        for rec in self:
            rec.session_id = rec.result_template_id.session_id

    def action_validated(self):
        for rec in self:
            rec.state = 'validated'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.depends('line_ids', 'line_ids.state')
    def compute_total_result(self):
        total_pass = 0
        total_fail = 0
        for rec in self:
            for line_id in rec.line_ids:
                if line_id.state == 'pass':
                    total_pass += 1
                elif line_id.state == 'fail':
                    total_fail += 1
            rec.total_fail = total_fail
            rec.total_pass = total_pass


class StudentMarksheetLine(models.Model):
    _name = 'student.marksheet.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Marksheet Line Line"
    _rec_name = 'student_id'

    _sql_constraints = [
        ('result_template_name_uniq', 'unique (student_id,marksheet_id)',
         'Student should be unique for per marksheet.')
    ]

    marksheet_id = fields.Many2one('student.marksheet', string='Marksheet', tracking=True)
    student_id = fields.Many2one('university.student', string='Student', tracking=True)
    state = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string="Status",
                             tracking=True,compute="compute_total_marks",store=True)
    total_marks = fields.Float(string='Total Marks', compute="compute_total_marks", store=True)
    percentage = fields.Float(string='Percentage', compute="compute_total_marks", store=True)

    student_result_ids = fields.One2many('student.result', 'marksheet_line_id', string="Exam Attendance")
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.onchange('marksheet_id')
    def onchange_marksheet_id(self):
        for rec in self:
            rec.course_id = rec.marksheet_id.session_id.course_id
            rec.batch_id = rec.marksheet_id.session_id.batch_id

    @api.depends('student_result_ids', 'student_result_ids.marks','marksheet_id.pass_mark')
    def compute_total_marks(self):
        total_marks = 0
        state = False
        for rec in self:
            for line_id in rec.student_result_ids:
                total_marks += line_id.marks
                if line_id.marks < rec.marksheet_id.pass_mark:
                    state = 'fail'
            rec.total_marks = total_marks
            if state == 'fail':
                rec.state = state
            else:
                rec.state = 'pass'
            if len(rec.student_result_ids) > 0:
                rec.percentage = total_marks / len(rec.student_result_ids)


class StudentResult(models.Model):
    _name = 'student.result'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Result Line"
    _rec_name = 'student_id'

    student_id = fields.Many2one('university.student', string='Student', tracking=True,
                                 related='marksheet_line_id.student_id', store=True)
    marksheet_line_id = fields.Many2one('student.marksheet.line', string='Marksheet Line', tracking=True)
    exam_id = fields.Many2one('exam.exam', string='Exam', tracking=True)
    subject_id = fields.Many2one('university.subject', string='Subject')
    state = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string="Status",
                             tracking=True,compute='compute_status',store=True)
    marks = fields.Float(string="Marks")

    @api.depends('marksheet_line_id.marksheet_id.pass_mark', 'marks')
    def compute_status(self):
        for rec in self:
            if rec.marks >= rec.marksheet_line_id.marksheet_id.pass_mark:
                rec.state = 'pass'
            else:
                rec.state = 'fail'

    @api.onchange('exam_id')
    def onchange_exam_id(self):
        for rec in self:
            rec.subject_id = rec.exam_id.subject_id
