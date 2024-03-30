# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StudentParent(models.Model):
    _name = 'student.parent'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Parent"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('parents_name_uniq', 'unique (name,mobile,email,date_of_birth)', 'parent should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    pre = fields.Char(string="pre", compute='_compute_pre')
    mobile = fields.Char(string='Mobile', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    relation_id = fields.Many2one('parent.relationship', string="Relationship")

    @api.depends('gender')
    def _compute_pre(self):
        for rec in self:
            if rec.gender == 'male':
                rec.pre = 'Mrs'
            elif rec.gender == 'female':
                rec.pre = 'Miss'
            else:
                rec.pre = ''
