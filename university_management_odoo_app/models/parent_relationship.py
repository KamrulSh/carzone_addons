# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ParentRelationship(models.Model):
    _name = 'parent.relationship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Parent Relationship"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('parent_relationship_name_uniq', 'unique (name)', 'Relationship should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
