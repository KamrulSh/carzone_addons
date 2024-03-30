# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class UniversitySubject(models.Model):
    _name = 'university.subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Subject"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('subject_name_uniq', 'unique (name)', 'Subject should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)
    type = fields.Selection([('theory', 'Theory'), ('practical', 'Practical')], string="Type")
    subject_type = fields.Selection([('compulsory', 'Compulsory'), ('optional', 'Optional')], string="Subject Type")
    grade = fields.Float(string="Grade Weightage")
    department_id = fields.Many2one('hr.department', string="Department")
    course_ids = fields.Many2many('university.course', 'rel_uni_subject_course', 'subject_id', 'course_id',
                                  string='Course')
