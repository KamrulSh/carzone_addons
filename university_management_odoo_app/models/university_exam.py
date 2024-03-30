# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UniversityExam(models.Model):
    _name = 'university.exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Session"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_session_name_uniq', 'unique (name)', 'Exam Session should be unique.')
    ]

    name = fields.Char(string='Exam Session', tracking=True)
    code = fields.Char(string='Exam Session Code', tracking=True)
    start_date = fields.Date(string="Start Date", )
    end_date = fields.Date(string="End Date", )
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")
    exam_type_id = fields.Many2one('exam.type', string="Exam Type")
    exam_ids = fields.One2many('exam.exam', 'session_id', string="Subject")
    hall_ticket_ids = fields.One2many('hall.ticket.details', 'session_id', string="Hall Tickets")
    state = fields.Selection([('draft', 'Draft'), ('held', 'Held'), ('done', 'Done')],
                             default='draft', tracking=True)

    def action_held(self):
        for rec in self:
            rec.state = 'held'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    @api.onchange('course_id')
    def onchange_course_id(self):
        for rec in self:
            student_ids = self.env['university.student'].search(
                [('course_id', '=', rec.course_id.id), ('active', '=', True)], order="name asc")
            rec.hall_ticket_ids.unlink()
            for student_id in student_ids:
                print(student_id.name)

                self.env['hall.ticket.details'].create({'student_id': student_id.id,
                                                        'session_id': rec.id,
                                                        })


class ExamExam(models.Model):
    _name = 'exam.exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Attendance Line"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_session_exam_name_uniq', 'unique (name,session_id)', 'Exam should be unique for per Session.')
    ]

    session_id = fields.Many2one('university.exam', string='Exam Session', tracking=True)
    name = fields.Char(string='Name', tracking=True)
    subject_id = fields.Many2one('university.subject', string='Subject', tracking=True)
    start_date = fields.Datetime(string="Start Time")
    end_date = fields.Datetime(string="End Time")
    total_marks = fields.Float(string='Total Marks')
    pass_marks = fields.Float(string='Passing Marks')
    remarks = fields.Text(string="Remarks")
    state = fields.Selection([('draft', 'Draft'), ('held', 'Held'), ('upload', 'Result Upload'), ('done', 'Done')],
                             default='draft', tracking=True)
    attendance_ids = fields.One2many('exam.attendance', 'exam_id', string="Exam Attendance")
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")


    @api.onchange('session_id')
    def onchange_session_id(self):
        for rec in self:
            rec.course_id = rec.session_id.course_id
            rec.batch_id = rec.session_id.batch_id

    def action_held(self):
        for rec in self:
            rec.state = 'held'

    def action_upload(self):
        for rec in self:
            rec.state = 'upload'

    def action_done(self):
        for rec in self:
            rec.state = 'done'


class ExamAttendance(models.Model):
    _name = 'exam.attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Attendance"
    _rec_name = 'exam_id'

    _sql_constraints = [
        ('exam_session_exam_name_uniq', 'unique (student_id,exam_id)', 'Student should be unique for per Exam.')
    ]

    student_id = fields.Many2one('university.student', string='Student', tracking=True)
    exam_id = fields.Many2one('exam.exam', string='Exam', tracking=True)
    state = fields.Selection([('present', 'Present'), ('absent', 'Absent')], default='present', string="Status",
                             tracking=True)
    marks = fields.Float(string="Marks")
    remarks = fields.Text(string="Remarks")
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.onchange('exam_id')
    def onchange_exam_id(self):
        for rec in self:
            rec.course_id = rec.exam_id.session_id.course_id
            rec.batch_id = rec.exam_id.session_id.batch_id


class HallTicketDetails(models.Model):
    _name = 'hall.ticket.details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hall Ticket"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_session_exam_name_uniq', 'unique (student_id,session_id)', 'Student should be unique for per Session.')
    ]

    session_id = fields.Many2one('university.exam', string='Exam Session', tracking=True)
    student_id = fields.Many2one('university.student', string='Student', tracking=True)
    center_id = fields.Many2one('exam.center', string='Exam Center', tracking=True)
    block_id = fields.Many2one('exam.block', string='Exam Block', tracking=True)
    room_id = fields.Many2one('exam.room', string='Exam Room', tracking=True)
    name = fields.Char(string='Seat No', tracking=True)
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.onchange('session_id')
    def onchange_session_id(self):
        for rec in self:
            rec.course_id = rec.session_id.course_id
            rec.batch_id = rec.session_id.batch_id

