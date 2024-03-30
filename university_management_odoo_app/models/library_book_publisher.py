
from odoo import api, fields, models


class LibraryBookPublisher(models.Model):
    _name = 'library.book.publisher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book Publisher"
    _order = "name asc"
    _rec_name = 'name'

    _sql_constraints = [
        ('library_book_publisher_name_uniq', 'unique (name)', 'Publisher should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
