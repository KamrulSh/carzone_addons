# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AttendanceRegister(models.Model):
    _name = 'attendance.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Attendance Register"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('attendance_name_uniq', 'unique (name)', 'Attendance Register should be unique.')
    ]

    name = fields.Char(string='Name',tracking=True)
    code = fields.Char(string='Code',tracking=True)
    course_id = fields.Many2one('university.course',string="Course")
    batch_id = fields.Many2one('university.batch',string="Batch")
