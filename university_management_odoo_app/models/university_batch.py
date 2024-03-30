# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class UniversityBatch(models.Model):
    _name = 'university.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Batch"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('batch_name_uniq', 'unique (name,course_id)', 'Batch should be unique For per Course.')
    ]

    name = fields.Char(string='Name',tracking=True)
    code = fields.Char(string='Code',tracking=True)
    start_date = fields.Date(string='Start Date',tracking=True)
    end_date = fields.Date(string='End Date',tracking=True)
    course_id = fields.Many2one('university.course',string="Course")
