# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class UniversityCourse(models.Model):
    _name = 'university.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Course Management"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('course_name_uniq', 'unique (name)', 'Course should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    fees = fields.Float(string='Fess', tracking=True)
