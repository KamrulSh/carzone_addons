# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ExamType(models.Model):
    _name = 'exam.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Type"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_type_name_uniq', 'unique (name)', 'Exam Type should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
