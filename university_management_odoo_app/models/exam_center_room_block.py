# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ExamTCenter(models.Model):
    _name = 'exam.center'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Center"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_center_name_uniq', 'unique (name)', 'Exam Center should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)


class ExamBlock(models.Model):
    _name = 'exam.block'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Block"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_block_name_uniq', 'unique (name)', 'Exam Block should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)


class ExamRoom(models.Model):
    _name = 'exam.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam Room"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('exam_room_name_uniq', 'unique (name)', 'Exam Room should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
