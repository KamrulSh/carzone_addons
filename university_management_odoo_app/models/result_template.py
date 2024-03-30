# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResultTemplate(models.Model):
    _name = 'result.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Result"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('result_template_name_uniq', 'unique (name)', 'Result Template should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    session_id = fields.Many2one('university.exam', string='Exam Session', tracking=True)
    date = fields.Date(string='Result Date')
