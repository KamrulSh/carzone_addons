from odoo import api, fields, models


class AssignmentType(models.Model):
    _name = 'assignment.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Assignment Type"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('assignment_type_name_uniq', 'unique (name)', 'Assignment Type should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)