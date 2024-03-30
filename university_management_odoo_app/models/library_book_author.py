
from odoo import api, fields, models


class LibraryBookAuthor(models.Model):
    _name = 'library.book.author'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book Author"
    _order = "id desc"
    _rec_name = 'name'

    _sql_constraints = [
        ('library_book_author_name_uniq', 'unique (name)', 'Author Name should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
