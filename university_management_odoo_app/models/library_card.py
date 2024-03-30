
from odoo import api, fields, models


class LibraryCard(models.Model):
    _name = 'library.card'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Card"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('library_card_name_uniq', 'unique (name)', 'Assignment Type should be unique.')
    ]

    name = fields.Char(string='Number', tracking=True)
    issue_date = fields.Date(string='Issue Date', tracking=True)
    type = fields.Selection([('student', 'student'), ('faculty', 'Faculty')], tracking=True,default='student')
    student_id = fields.Many2one('university.student', string="Student", tracking=True)
    faculty_id = fields.Many2one('university.faculty', string="Faculty", tracking=True)


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('library.card') or 'New'
        return super(LibraryCard, self).create(vals)
