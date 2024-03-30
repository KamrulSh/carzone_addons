# Copyright 2015 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StudentHallTicket(models.TransientModel):
    _name = 'student.hall.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student Hall Ticket"

    session_id = fields.Many2one('university.exam', string='Exam Session')
    student_id = fields.Many2one('university.student', string='Student')
    name = fields.Char(string="Seat No")
    center_id = fields.Many2one('exam.center', string='Exam Center', tracking=True)
    block_id = fields.Many2one('exam.block', string='Exam Block', tracking=True)
    room_id = fields.Many2one('exam.room', string='Exam Room', tracking=True)
    course_id = fields.Many2one('university.course', string="Course")
    batch_id = fields.Many2one('university.batch', string="Batch")

    @api.model
    def default_get(self, fields):
        res = super(StudentHallTicket, self).default_get(fields)
        user_id = self.env.user
        print(user_id.name, "User")
        student_id = self.env['university.student'].search([('user_id', '=', user_id.id)], limit=1)
        print(student_id.name, "Hello")
        res['student_id'] = student_id.id
        return res

    def action_download(self):
        print("Hello")
        # return self.pool['report'].get_action('university_management_odoo_app.report_student_hall_ticket')

        return self.env.ref('university_management_odoo_app.action_student_hall_ticket').report_action(self)

    @api.onchange('student_id','session_id')
    def onchange_student_id(self):
        for rec in self:
            rec.name=''
            rec.center_id = False
            rec.block_id = False
            rec.room_id = False
            rec.course_id = False
            rec.batch_id = False
            rec.course_id = rec.session_id.course_id
            rec.batch_id = rec.session_id.batch_id
            hall_ticket_ids = self.env['hall.ticket.details'].search(
                [('session_id', '=', rec.session_id.id), ('student_id', '=', rec.student_id.id)],limit=1)
            for hall in hall_ticket_ids:
                rec.name = hall.name
                rec.center_id = hall.center_id
                rec.block_id = hall.block_id
                rec.room_id = hall.room_id

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('student.hall.ticket') or 'New'
    #     return super(StudentHallTicket, self).create(vals)
