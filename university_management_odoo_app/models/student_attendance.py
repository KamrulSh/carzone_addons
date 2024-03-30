# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Attendance"
    _rec_name = 'name'

    _sql_constraints = [
        ('student_attendance_name_uniq', 'unique (name,register_id)', 'name should be unique for per register.')
    ]

    name = fields.Char(string='Name', tracking=True)
    register_id = fields.Many2one('attendance.register', string="Register", tracking=True)
    session = fields.Char(string="Session")
    date = fields.Date(string="Date")
    line_ids = fields.One2many('student.attendance.line', 'attendance_id', string="Subject")
    state = fields.Selection([('draft', 'Draft'), ('start', 'Attendance Start'), ('taken', 'Attendance Taken')],
                             default='draft', tracking=True)

    def action_attendance_start(self):
        for rec in self:
            rec.state = 'start'

    def action_attendance_taken(self):
        for rec in self:
            rec.state = 'taken'


class FacultySubject(models.Model):
    _name = 'student.attendance.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Attendance Line"

    _sql_constraints = [
        ('student_attendance_line_name_uniq', 'unique (student_id,attendance_id)', 'student should be unique for per Attendance Sheet.')
    ]

    attendance_id = fields.Many2one('student.attendance', string='Attendance', tracking=True)
    student_id = fields.Many2one('university.student', string='Student', tracking=True)
    present = fields.Boolean(string="Present", tracking=True)
    late = fields.Boolean(string="Late", tracking=True)
    absent_excused = fields.Boolean(string="Absent Excused", tracking=True)
    absent_unexcused = fields.Boolean(string="Absent Unexcused", tracking=True)
    remarks = fields.Text(string="Remarks")
    date = fields.Date(string="Date")
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.onchange('attendance_id')
    def onchange_attendance_id(self):
        for rec in self:
            rec.date = rec.attendance_id.date
            rec.course_id = rec.attendance_id.register_id.course_id
            rec.batch_id = rec.attendance_id.register_id.batch_id
