# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class UniversityDepartment(models.Model):
    _name = 'university.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Department"
    _order = "name asc"
    _rec_name = 'name'

    name = fields.Char(string='Name',tracking=True)