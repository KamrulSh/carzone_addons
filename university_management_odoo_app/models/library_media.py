
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryMedia(models.Model):
    _name = 'library.media'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Media"
    _rec_name = 'name'

    _sql_constraints = [
        ('library_media_name_uniq', 'unique (name)', 'Library Media should be unique.')
    ]

    name = fields.Char(string='Name', tracking=True)
    edition = fields.Char(string='Edition', tracking=True)
    author_ids = fields.Many2many('library.book.author', 'rel_book_author_library_media', 'media_id', 'author_id',
                                  string="Author")
    publisher_ids = fields.Many2many('library.book.publisher', 'rel_book_publisher_library_media', 'media_id',
                                     'publisher_id', string="Publisher")
    isbn_code = fields.Char('ISBN Code')
    internal_code = fields.Char('Internal Code')
    unit_ids = fields.One2many('media.unit', 'media_id', string="Unit")
    movement_ids = fields.One2many('student.library', 'media_id', string="Movement")
    queue_request_ids = fields.One2many('media.queue.request', 'media_id', string="Queue Request")
    remarks = fields.Text('Description')


class MediaUnit(models.Model):
    _name = 'media.unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Media Unit"
    _rec_name = 'name'

    media_id = fields.Many2one('library.media', string='Media')
    name = fields.Char(string='Name', tracking=True)
    barcode = fields.Char(string='Barcode', tracking=True)
    state = fields.Selection([('issue', 'Issue'), ('available', 'Available')], string="State", default='available')

    _sql_constraints = [
        ('library_media_unit_name_uniq', 'unique (name)', 'Media unit should be unique per media.')
    ]


class MediaQueueRequest(models.Model):
    _name = 'media.queue.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Media Queue Request"
    _rec_name = 'name'

    media_id = fields.Many2one('library.media', string='Media')
    name = fields.Char(string='Name', tracking=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection([('request', 'Request'), ('accept', 'Accept'), ('reject', 'Reject')], default='request',
                             string="State")

    def action_accept(self):
        for rec in self:
            rec.state = 'accept'

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('media.queue.request') or 'New'
        return super(MediaQueueRequest, self).create(vals)


class MediaPurchaseRequest(models.Model):
    _name = 'media.purchase.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Media Queue Request"
    _rec_name = 'name'

    name = fields.Char(string='Title', tracking=True)
    user_id = fields.Many2one('res.users',string="Requested by", default=lambda self: self.env.user.id)
    author_id = fields.Many2one('library.book.author', string="Author")
    publisher_id = fields.Many2one('library.book.publisher', string="Publisher")
    course_id = fields.Many2one('university.course', string="Course")
    subject_id = fields.Many2one('university.subject', string="Subject")
    edition = fields.Char(string='Edition')
    state = fields.Selection([('draft', 'Draft'), ('request', 'Request'), ('accept', 'Accept'), ('reject', 'Reject')],
                             default='draft',
                             string="State")

    def action_request(self):
        for rec in self:
            rec.state = 'request'

    def action_accept(self):
        for rec in self:
            rec.state = 'accept'

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'
